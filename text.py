def parse_name(name):
    clean_name = name.replace("_", " ").replace("-", " ").title()

    # if clean name exactly equals "id" or "pk" then uppercase
    if clean_name in ["id", "pk"]:
        clean_name = clean_name.upper()
    # if clean name ends with " id" or "pk" then uppercase "id" or "pk"
    elif clean_name.endswith(" id") or clean_name.endswith("pk"):
        clean_name = clean_name[:-2] + clean_name[-2:].upper()

    return clean_name


def clean_view_name(string):
    return string.replace("_av", "").replace("av_", "")


def build_sql_reference(project, dataset, name):
    return f"{project}.{dataset}.{name}"


def create_view_name(string) -> str:
    output = clean_view_name(string)
    output = parse_name(output)
    return output
