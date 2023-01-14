import json


def pretty_labels(name):
    clean_name = name.replace("_", " ").replace("-", " ").title()

    # if clean name exactly equals "id" or "pk" then uppercase
    if clean_name in ["Id", "Pk"]:
        clean_name = clean_name.upper()
    # if clean name ends with " id" or "pk" then uppercase "id" or "pk"
    if clean_name.endswith(" id") or clean_name.endswith("pk"):
        clean_name = clean_name[:-2] + clean_name[-2:].upper()

    if clean_name.endswith("_tstamp"):
        clean_name = clean_name.split("_tstamp")[0]

    return clean_name


def clean_view_name(string):
    return string.replace("_av", "").replace("av_", "")


def build_sql_reference(project, dataset, name):
    return f"{project}.{dataset}.{name}"


def create_view_name(string) -> str:
    output = clean_view_name(string)
    output = pretty_labels(output)
    return output


def pretty_print(obj):
    print(json.dumps(obj, indent=4))
