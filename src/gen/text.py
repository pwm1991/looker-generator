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
    if string.startswith("date") and string.lower() != "dates":
        output = string[4:]
    if string.endswith("tstamp"):
        output = string[:-6]
    # if name starts or ends with "time" remove "time" from the label name
    if string.startswith("time"):
        output = string[4:]
    return remove_multiple_spaces(output)


def remove_multiple_spaces(string):
    return " ".join(string.split())


def beautify_abbreviation(string):
    output = string

    abbreviations = [
        "pk",
        "id",
        "fk",
        "sk",
        "guid",
        "utc",
        "gmt",
        "gbp",
        "usd",
        "dau",
        "wau",
        "mau",
        "Deu",
        "Weu",
        "Meu",
        "Rweu",
        "idfa",
        "idfv",
        "os",
    ]

    test_string = string.lower()

    if test_string in abbreviations:
        return output.upper()

    for abbr in abbreviations:
        mid_string_test = " " + abbr + " "
        mid_string_test_as_title = mid_string_test.title()
        abbr_len = len(abbr)

        if test_string.endswith(abbr):
            output = output[:-abbr_len] + abbr.upper()

        if mid_string_test in test_string:
            output = output.replace(mid_string_test_as_title, mid_string_test.upper())

    return output


def set_field_label(name):

    output = convert_to_string_case(name).strip()

    # if name contains " id " then race " id " to " ID

    # if name starts or ends with "date" remove date

    output = convert_to_string_case(output)
    output = remove_multiple_spaces(output)
    output = clean_date(output)
    output = output.replace(".", " ")
    output = output.title()
    output = output.strip()
    output = beautify_abbreviation(output)

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
