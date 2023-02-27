import os
import yaml
from src.api.bigquery import BigQueryTableReference
from src.api.validate_config import validate_view_references
from src.gen.create_view import GenerateView
from google.cloud import bigquery


env_project = "ct-looker-staging"


def load_schema(file: str):
    print(f"Loading schema from {file}")
    with open(file, "r") as f:
        try:
            schema = yaml.load(f, Loader=yaml.FullLoader)
            print(f"Loaded schema from {file}")
            return dict(schema["views"])
        except yaml.YAMLError as exc:
            print(exc)


def get_files():
    directory = os.listdir("views")

    print("Processing files")
    files = [file for file in directory if file.endswith(".yaml")]

    if len(files) == 0:
        print("No files found")
        exit()
    print(f"Found {len(files)} files")
    return files


def get_views():
    files = get_files()

    views = []

    for file in files:
        load_schemas = load_schema(f"views/{file}")
        if load_schemas is None:
            raise Exception(f"Error loading schemas from {file}")

        views_to_process = load_schemas

        validation = validate_view_references(views_to_process)

        disabled_views = [
            view for view in views_to_process if view.get("disabled") == True
        ]
        if len(disabled_views) > 0:
            print(f"Found {len(disabled_views)} disabled views")
            print(", ".join([view["reference"] for view in disabled_views]))

        for view in views_to_process:
            if view in disabled_views:
                continue
            print(f"Processing {view['reference']}")
            views.append(view)

    return views


def main():
    client = bigquery.Client(project=env_project)

    views_to_process = get_views()

    for view in views_to_process:

        print(f"Processing {view['reference']}")

        bigquery_get_table = client.get_table(view["reference"])

        bigquery_schema = BigQueryTableReference(bigquery_get_table, view)

        GenerateView(bigquery_schema).to_lookml()
