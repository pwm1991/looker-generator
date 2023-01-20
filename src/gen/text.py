import json


def convert_to_string_case(string):
    return string.replace("_", " ").replace("-", " ")


def convert_to_snake_case(string: str) -> str:
    return string.replace(" ", "_").replace("-", "_").lower()


def title_pk(string):
    if string.lower() in ["pk", "id", "fk", "sk"]:
        return string.upper()
    return string


# return quoted string
def quote_string(string):
    return f'"{string}"'


def remove_tstamp(string):
    return string.split(" tstamp")[0]


def remove_multiple_spaces(string):
    return " ".join(string.split())


def gen_field_label(name):
    pk = ["pk", "id", "fk", "sk"]
    output = convert_to_string_case(name)

    output = title_pk(output)
    if name.lower() in pk:
        return output

    # if name starts or ends with "date" remove date
    if output.lower().startswith("date"):
        output = output[4:]
    if output.lower().endswith("date"):
        output = output[:-4]
    # if name starts or ends with "time" remove time
    if output.lower().startswith("time"):
        output = output[4:]

    output = convert_to_string_case(output)
    output = remove_tstamp(output)
    output = remove_multiple_spaces(output)
    output = output.replace(".", " ")
    output = output.title()
    output = output.strip()

    # check string ends with an identifier, and upper case it
    for a in pk:

        if output.lower().endswith(a):
            output = output[:-2] + a.upper()

    return output


def gen_view_name(string):
    for l in ["_av", "av_"]:
        string = string.replace(l, "")
    for l in ["  "]:
        string = string.replace(l, " ")
    return string


def pretty_print(input):
    # if input is a string
    if isinstance(input, str):
        print(input)
    elif isinstance(input, dict):
        print(json.dumps(input, indent=4))
