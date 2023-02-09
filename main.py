import os
import yaml
from dotenv import dotenv_values
from src.api.bigquery import BigQueryTableReference
from src.gen.create_view import GenerateView
from google.cloud import bigquery

config = dotenv_values(".env")

# Function that loads schema from a json file
def load_schema(file):
    print(f"Loading schema from {file}")
    # open yaml file
    schema = ""
    # load yaml file
    with open(file, "r") as f:
        schema = yaml.load(f, Loader=yaml.FullLoader)

    print(f"Returning schema")
    return dict(schema)


def get_files():
    directory = os.listdir("views")

    files = []

    print("Getting files")

    for file in directory:
        if file.endswith(".yaml"):
            files.append(file)
    if len(files) == 0:
        print("No files found")
        exit()
    print(f"Found {len(files)} files")
    return files


def main():
    client = bigquery.Client(project="ct-looker-staging")
    files = get_files()
    for file in files:
        properties = load_schema(f"views/{file}")
        for view in properties["views"]:
            if view.get("disabled") == True:
                print(f"Skipping {view['reference']}: marked as disabled")
                continue

            print(f"Getting schema for {view['reference']} from BigQuery")

            bigquery_get_table = client.get_table(view["reference"])

            bigquery_schema = BigQueryTableReference(bigquery_get_table, view)

            GenerateView(bigquery_schema).to_lookml()
            print("Done")


main()
