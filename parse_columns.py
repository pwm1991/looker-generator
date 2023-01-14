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


def parse_field(dim, nested_mode=False):

    definition = {
        "name": dim["column_name"].lower(),
        "label": parse_name(dim["column_name"]),
        "sql": dim["column_name"],
        "metadata": {},
    }

    if dim["data_type"] != "REPEATED":
        definition["type"] = type_parser(dim["data_type"])

    if nested_mode == False:
        definition["sql"] = f"${{TABLE}}.{definition['sql']}"

    if definition["type"] == "time":
        definition["timeframes"] = looker_timeframes

    if dim["data_type"] in remove_timezones:
        definition["convert_tz"] = "no"
        definition["timeframes"].remove("time")

    # if dimension has description add to parsed
    if dim.get("description") is not None:
        definition["description"] = dim["description"]

    if dim.get("COLUMN_DEFAULT") is not None:
        definition["default_value"] = dim["COLUMN_DEFAULT"]

    if dim["is_nullable"] == "REPEATED" and dim["data_type"] == "RECORD":
        # Hide the root field
        definition["hidden"] = "yes"

        if dim.get("fields") is not None:

            definition["metadata"]["repeat_type"] = "complex"

            # Parse child fields
            definition["fields"] = parse_all_fields(dim["fields"], True)

            # Set group label
            updated_fields = []

            for field in definition["fields"]:
                new_field = field
                field["dimension"]["group_label"] = definition["label"]
                updated_fields.append(new_field)

            definition["fields"] = updated_fields

    if is_primary_key(dim["column_name"]):
        definition["primary_key"] = "yes"

    """
    If the field has already been processed, it'll be nested in a dimension
    prop already, therefore just return it. Else, add the dimension prop
    """
    if definition.get("defintiion") is not None:
        return definition
    return {"dimension": definition}


def parse_all_fields(fields, nested_mode=False):
    dimensions = []
    for field in fields:
        dimensions.append(parse_field(field, nested_mode))

    if len(dimensions) == 0:
        raise AssertionError("No fields parsed")

    return dimensions
