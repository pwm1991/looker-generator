import json


def convert_to_string_case(string):
    return string.replace("_", " ").replace("-", " ")


def convert_to_snake_case(string: str) -> str:
    return string.replace(" ", "_").replace("-", "_").lower()


# return quoted string
def quote_string(string):
    return f'"{string}"'


def clean_date(string):
    output = string.lower()
    if string.startswith("date"):
        output = string[4:]
    if string.endswith("tstamp"):
        output = string[:-5]
    # if name starts or ends with "time" remove "time" from the label name
    if string.startswith("time"):
        output = string[4:]
    return output


def remove_multiple_spaces(string):
    return " ".join(string.split())


def gen_field_label(name):
    primary_keys = ["pk", "id", "fk", "sk"]

    output = convert_to_string_case(name).strip()

    if name.lower() in primary_keys:
        return output.upper()

    # if name starts or ends with "date" remove date

    output = convert_to_string_case(output)
    output = remove_multiple_spaces(output)
    output = clean_date(output)
    output = output.replace(".", " ")
    output = output.title()
    output = output.strip()

    # check string ends with an identifier, and upper case it
    for str in primary_keys:
        if output.lower().endswith(str):
            output = output[:-2] + str.upper()

    return output


def gen_view_name(string):
    for l in ["av", "vw", "view"]:
        string = string.replace("_" + l, "")
        string = string.replace(l + "_", "")
        string = remove_multiple_spaces(string)
    return string


def pretty_print(input):
    # if input is a string
    if isinstance(input, str):
        print(input)
    elif isinstance(input, dict):
        print(json.dumps(input, indent=4))
