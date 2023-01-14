from text import pretty_label

parsed = []


def bigquery_type_to_looker(bigquery_type):

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
        raise raise_type_not_found(bigquery_type)
    return types[bigquery_type]


remove_timezones = ["DATE", "TIMESTAMP", "DATETIME"]

looker_timeframes = ["raw", "time", "date", "week", "month", "quarter", "year"]


def raise_type_not_found(type):
    return TypeError(f"Type {type} not in types")


def is_primary_key(name):
    # check if name is in a list of primary keys
    return name in ["id", "primary_key", "pk"]


def parse_field(dim, nested_mode=False):

    definition = {
        "sql": dim["column_name"],
        "type": bigquery_type_to_looker(dim["data_type"]),
        "name": dim["column_name"].lower(),
        "label": pretty_label(dim["column_name"]),
    }

    if nested_mode == False:
        definition["sql"] = f"${{TABLE}}.{definition['sql']}"

    """Set timeframes if a time type"""
    if definition["type"] == "time":
        definition["timeframes"] = looker_timeframes

    """Remove timezones and time type if just a date"""
    if dim["data_type"] in remove_timezones:
        definition["convert_tz"] = "no"
        definition["timeframes"].remove("time")

    """Set description"""
    if dim.get("description") is not None:
        definition["description"] = dim["description"]

    """Set default value"""
    if dim.get("COLUMN_DEFAULT") is not None:
        definition["default_value"] = dim["COLUMN_DEFAULT"]

    """Set primary key"""
    if is_primary_key(dim["column_name"]):
        definition["primary_key"] = "yes"

    if dim["data_type"] in ["RECORD", "REPEATED"]:
        del definition["type"]
        definition["hidden"] = "yes"

        if dim.get("fields") is not None:
            definition["nested_view"] = {
                "view_name": dim["column_name"],
                "dimensions": parse_all_fields(dim["fields"], True),
            }

    return definition


def parse_all_fields(fields, nested_mode=False):
    dimensions = []
    for field in fields:
        dimensions.append(parse_field(field, nested_mode))

    if len(dimensions) == 0:
        raise AssertionError("No fields parsed")

    return dimensions
