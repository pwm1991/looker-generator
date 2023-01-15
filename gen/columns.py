from gen.text import pretty_label
from gen.looker_utils import bigquery_type_to_looker


def set_looker_timeframes(type, data_type) -> dict:

    looker_timeframes = ["raw", "time", "date", "week", "month", "quarter", "year"]
    response = {"convert_tz": "no", "timeframes": looker_timeframes}
    if type == "time":
        return response
    elif data_type in ["DATE", "TIMESTAMP", "DATETIME"]:
        return dict(response, *{"timeframes": looker_timeframes.remove("time")})


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

    if definition["type"] in ["time", "date"]:
        timeframes = set_looker_timeframes(definition["type"], dim["data_type"])
        definition = dict(definition, **timeframes)

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
            dimensions = parse_all_fields(dim["fields"], True)
            group_label = pretty_label(dim["column_name"])

            # add group_label key to each dimension in dimensions
            dimensions = [
                dict(dimension, **{"group_label": group_label}) for dimension in dimensions
            ]

            definition["nested_view"] = {"view_name": dim["column_name"], "dimensions": dimensions}

    return definition


def parse_all_fields(fields, nested_mode=False):
    dimensions = []
    for field in fields:
        dimensions.append(parse_field(field, nested_mode))

    if len(dimensions) == 0:
        raise AssertionError("No fields parsed")

    return dimensions
