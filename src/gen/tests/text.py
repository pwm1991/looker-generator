import json


def pretty_label(name):
    output = name.replace("_", " ").replace("-", " ").title()

    # if clean name exactly equals "id" or "pk" then uppercase
    if output.lower() in ["id", "pk", "fk", "sk"]:
        output = output.upper()
    # if clean name ends with " id" or "pk" then uppercase "id" or "pk"
    if output.endswith(" Id") or output.endswith("Pk"):
        output = output[:-2] + output[-2:].upper()

    if output.endswith(" Tstamp"):
        output = output.split(" Tstamp")[0]

    # remove 2 or more spaces in string
    output = " ".join(output.split())

    return output


def clean_view_name(string):
    for l in ["_av", "av_"]:
        string = string.replace(l, "")
    for l in ["  "]:
        string = string.replace(l, " ")
    return string


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


def looker_reference(string) -> str:
    # replace -,_," " with _
    # lowercase
    for l in ["-", " "]:
        string = string.replace(l, "_")
    return string.lower()


def safe_filename(filen) -> str:
    if filen.endswith(".view.lkml") is False:
        filen = filen + ".view.lkml"
    return filen.replace(" ", "_").replace("-", "_").lower()


def pretty_print(input):
    # if input is a string
    if isinstance(input, str):
        print(input)
    elif isinstance(input, dict):
        print(json.dumps(input, indent=4))
