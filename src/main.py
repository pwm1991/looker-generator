import os
import json
import logging
from gen.create_view import GenerateView

# Function that loads schema from a json file
def load_schema(file):
    print(f"Loading schema from {file}")
    with open(file, "r") as read_file:
        schema = json.load(read_file)
    return schema


# loop through yaml files in views folder


def get_files():
    directory = os.listdir("views")

    files = []

    for file in directory:
        if file.endswith(".json"):
            files.append(file)
    return files


def main():
    files = get_files()
    for file in files:
        if file == "example-with-2-repeated-records.json":
            schema = load_schema(f"views/{file}")
            new_schema = GenerateView(schema)
            new_schema.to_lookml()


main()
