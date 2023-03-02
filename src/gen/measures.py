"""
It needs to:
* Take a type of measure = number
* Apply a count and sum for each metric
* Prepend m_ infront of the name.
* Remove ${TABLE} from the sql and convert to reference
* Try to update the description
* Try to apply a value_format_name depending on the metric
"""
examples = [
    {
        "name": "app__build",
        "sql": "${TABLE}.app.build",
        "label": "App Build",
        "group_label": "App",
        "type": "number",
        "field_type": "dimension",
    },
    {
        "name": "actuals_global_value_mtd_py",
        "sql": "${TABLE}.actuals_global_value_mtd_py",
        "label": "Actuals Global Value Mtd Py",
        "type": "number",
    },
]
