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


def raise_type_not_found(type):
    return TypeError(f"Type {type} not in types")
