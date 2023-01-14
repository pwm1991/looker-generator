from text import parse_name

parsed = []


def type_parser(type):

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
    if type not in types:
        raise raise_type_not_found(type)
    return types[type]


remove_timezones = ["DATE", "TIMESTAMP", "DATETIME"]

looker_timeframes = ["raw", "time", "date", "week", "month", "quarter", "year"]


def raise_type_not_found(type):
    return TypeError(f"Type {type} not in types")


def is_primary_key(name):
    # check if name is in a list of primary keys
    return name in ["id", "primary_key", "pk"]


def parse_field(dimension, nested_mode=False):

    parsed = {
        "name": dimension["column_name"].lower(),
        "label": parse_name(dimension["column_name"]),
        "type": type_parser(dimension["data_type"]),
        "sql": f'{dimension["column_name"]}',
        "metadata": {},
    }

    if parsed["type"] == "time":
        parsed["timeframes"] = looker_timeframes

    if dimension["data_type"] in remove_timezones:
        parsed["convert_tz"] = "no"
        parsed["timeframes"].remove("time")

    # if dimension has description add to parsed
    if dimension.get("description") is not None:
        parsed["description"] = dimension["description"]

    if dimension.get("COLUMN_DEFAULT") is not None:
        parsed["default_value"] = dimension["COLUMN_DEFAULT"]

    if dimension["is_nullable"] == "REPEATED" and dimension["data_type"] == "RECORD":
        # Hide the root field
        parsed["hidden"] = "yes"

        if dimension.get("fields") is not None:
            # Parse child fields
            parsed["fields"] = parse_all_fields(dimension["fields"], True)

            # Set group label
            for field in parsed["fields"]:
                field["group_label"] = parsed["label"]
                parsed["metadata"]["repeat_type"] = "complex"
        else:
            # Repeated, but simply a list of values
            parsed["metadata"]["repeat_type"] = "simple"

    if nested_mode == False:
        parsed["sql"] = f"${{TABLE}}.{parsed['sql']}"

    if is_primary_key(dimension["column_name"]):
        parsed["primary_key"] = "yes"

    return {"dimension": parsed}


def parse_all_fields(fields, nested_mode=False):
    parsed = []
    for field in fields:
        parsed.append(parse_field(field, nested_mode))

    return parsed
