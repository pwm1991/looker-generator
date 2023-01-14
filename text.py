def parse_name(name):
    return name.replace("_", " ").replace("-", " ").title()


def clean_view_name(string):
    return string.replace("_av", "").replace("av_", "")


def build_sql_reference(project, dataset, name):
    return f"{project}.{dataset}.{name}"


def create_view_name(string) -> str:
    output = clean_view_name(string)
    output = parse_name(output)
    return output
