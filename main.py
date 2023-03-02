import os
import yaml
from src.api.bigquery import BigQueryTableReference
from src.api.validate_config import validate_view_references
from src.gen.create_view import GenerateView
from src.config_validation.validate import validate_configs
from google.cloud import bigquery

from dotenv import load_dotenv

load_dotenv()

BIGQUERY_PROJECT = os.getenv("BIGQUERY_PROJECT")
CONFIG_DIRECTORY = (os.getenv("CONFIG_DIRECTORY") or "").replace("/", "")


def load_schema(file: str):
    print(f"Loading schema from {file}")
    with open(file, "r") as f:
        try:
            schema = yaml.load(f, Loader=yaml.FullLoader)
            print(f"Loaded schema from {file}")
            return schema["views"]
        except yaml.YAMLError as exc:
            print(exc)


def get_files():
    directory = os.listdir(f"{CONFIG_DIRECTORY}")

    print("Processing files")
    files = [
        file
        for file in directory
        if file.endswith(".yaml") and not file.startswith("example")
    ]

    if len(files) == 0:
        print("No files found")
        exit()
    print(f"Found {len(files)} files")
    return files


def get_views():
    files = get_files()

    views = []

    for file in files:
        load_schemas = load_schema(f"{CONFIG_DIRECTORY}/{file}")
        if load_schemas is None:
            raise Exception(f"Error loading schemas from {file}")

        views_to_process = validate_configs(BIGQUERY_PROJECT, load_schemas, "SKIP")

        for view in views_to_process:
            print(f"Processing {view['reference']}")
            views.append(view)

    return views


def build_views():
    client = bigquery.Client(project=BIGQUERY_PROJECT)

    views_to_process = get_views()

    for view in views_to_process:

        print(f"Processing {view['reference']}")

        bigquery_get_table = client.get_table(view["reference"])

        bigquery_schema = BigQueryTableReference(bigquery_get_table, view)

        GenerateView(bigquery_schema).to_lookml()


build_views()
