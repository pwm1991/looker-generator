import json


def pretty_label(name):
    input_name = name.lower()
    output = input_name.replace("_", " ").replace("-", " ").title()

    # if clean name exactly equals "id" or "pk" then uppercase
    if input_name.lower() in ["id", "pk", "fk", "sk"]:
        output = output.upper()
    # if clean name ends with " id" or "pk" then uppercase "id" or "pk"
    if input_name.endswith(" Id") or input_name.endswith("Pk"):
        output = output[:-2] + output[-2:].upper()

    if output.endswith(" Tstamp"):
        output = output.split(" Tstamp")[0]

    return output


def clean_view_name(string):
    return string.replace("_av", "").replace("av_", "")


def build_sql_reference(table_reference: dict):
    # join list of strings with "."

    return (".").join(
        [
            table_reference["projectId"],
            table_reference["datasetId"],
            table_reference["tableId"],
        ]
    )


def create_view_name(string) -> str:
    output = clean_view_name(string)
    output = pretty_label(output)
    return output


def pretty_print(input):
    # if input is a string
    if isinstance(input, str):
        print(input)
    elif isinstance(input, dict):
        print(json.dumps(input, indent=4))
