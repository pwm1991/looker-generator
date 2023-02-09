import datetime
from textwrap import dedent
from src.gen.errors import LookerColumnTypeNotFound

looker_timeframes = ["raw", "time", "date", "week", "month", "quarter", "year"]

valid_looker_field_types = [
    "name",
    "sql",
    "primary_key",
    "type",
    "description",
    "label",
    "group_label",
    "timeframes",
    "convert_tz",
    "nested_mode",
    "hidden",
    "field_type",
    "input_schema",
    "nested_properties",
]


def looker_file_disclaimer(objects_in_file):

    total_object_bullet = ""
    if objects_in_file > 1:
        total_object_bullet = f"There are {objects_in_file} objects in this file."
    else:
        total_object_bullet = f"There is {objects_in_file} object in this file."

    # timestamp to nearest second
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return dedent(
        f"""
    # This file is auto-generated by the Looker Generator.
    # Do not edit this file directly, as it will be overridden.
    # Instead, extend this Looker file in a separate file.
    # - Generated at: {now}
    # - {total_object_bullet}

    """
    )


def bool_to_string(bool):
    if bool == True:
        return "yes"
    else:
        return "no"


def bigquery_type_to_looker_type(bigquery_type):

    bigquery_type = bigquery_type.upper()

    types = {
        "STRING": "string",
        "BOOLEAN": "yesno",
        "NUMERIC": "number",
        "FLOAT": "number",
        "INTEGER": "number",
        "DATE": "time",
        "TIME": "time",
        "TIMESTAMP": "time",
        "DATETIME": "time",
        "RECORD": None,
    }
    # when type not in types, raise exception
    if bigquery_type not in types:
        raise LookerColumnTypeNotFound(bigquery_type)
    return types[bigquery_type]


def filter_invalid_looker_properties(obj):

    # Keep field_type here so that it can be sorted later
    invalid_keys = [
        "input_schema",
        "nested_mode",
        "nested_view",
        "dimensions",
        "nested_properties",
        "field_type",
    ]

    output = {k: v for k, v in obj.items() if k not in invalid_keys}

    # Soft warn that some keys are not valid
    for k in obj.items():
        if k[0] not in valid_looker_field_types:
            print(
                f"WARNING: {k[0]} might not be a valid Looker field type. If you see this error persistently, update valid_looker_field_types"
            )

    return output