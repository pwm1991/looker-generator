import json
from generator import GenerateView

# Function that loads schema from a json file
def load_schema(file):
    schema = json.load(open(file))
    return schema


def main():
    schema = load_schema("example.json")

    new_schema = GenerateView(schema)
    new_schema.to_lookml()


main()
