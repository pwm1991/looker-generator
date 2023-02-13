from src.gen.text import set_field_label
from src.gen.looker import (
    bigquery_type_to_looker_type,
    looker_timeframes,
    bool_to_string,
)


class Dimension:
    def __init__(
        self, input_schema, primary_key, nested_mode=False, nested_metadata=None
    ):
        self.nested_mode = nested_mode
        self.nested_metadata = nested_metadata
        self.input_primary_key = primary_key
        self.input_schema = input_schema
        self.looker_property = {
            "name": input_schema["name"].lower(),
            "sql": self._set_sql_reference(),
            "description": input_schema.get("description") or None,
            "label": set_field_label(input_schema["name"]),
            "group_label": None,
            "primary_key": None,
            "type": bigquery_type_to_looker_type(input_schema["type"]),
            "timeframes": None,
            "field_type": "dimension",
        }

        if self.looker_property["name"] == "app__version":
            print("build column!")

        self._set_primary_key()
        self._set_time()
        self._set_group_label()

        if self.input_schema["type"] in ["RECORD"]:
            self._handle_repeated_fields()

    def _set_sql_reference(self):
        if self.nested_mode == False:
            if self.input_schema.get("sql"):
                return f"${{TABLE}}.{self.input_schema['sql']}"
            else:
                return f"${{TABLE}}.{self.input_schema['name']}"
        else:
            return self.input_schema["name"].replace("__", ".")

    def _set_group_label(self):
        diagnostic_fields = ["event_id", "run_id"]
        if self.nested_metadata is not None:
            self.looker_property["group_label"] = self.nested_metadata["group_label"]

        if self.input_schema["type"] in ["RECORD"]:
            self.looker_property["group_label"] = self.looker_property["label"]

        if self.looker_property["name"] in diagnostic_fields:
            self.looker_property["group_label"] = "Diagnostic Fields"

    def _set_primary_key(self):
        if self.input_primary_key == self.looker_property["name"]:
            self.looker_property["primary_key"] = bool_to_string(True)

    def _set_time(self):
        times = looker_timeframes.copy()
        if self.input_schema["type"] in ["DATE"]:
            # remove time from timeframes
            times.remove("time")
            times.remove("raw")
            self.looker_property["timeframes"] = times
        elif self.input_schema["type"] in ["TIMESTAMP", "DATETIME", "EPOCH"]:
            self.looker_property["timeframes"] = looker_timeframes

        if self.looker_property["timeframes"] is not None:
            self.looker_property["field_type"] = "dimension_group"
            # Never convert the timezone for timeframes
            self.looker_property["convert_tz"] = "no"

    def _handle_repeated_fields(self):

        fields = self.input_schema.get("fields")

        is_repeated_field = False

        if self.input_schema.get("mode") in ["REPEATED"]:
            is_repeated_field = True
            self.looker_property["hidden"] = "yes"
            del self.looker_property["type"]
        else:
            self.looker_property["hidden"] = "yes"

        if fields is not None:
            if is_repeated_field == False:
                # For nested, non-repeating fields, prepend the parent input_schema.name
                for field in fields:
                    field["sql"] = f"{self.input_schema['name']}.{field['name']}"
                    field["name"] = f"{self.input_schema['name']}__{field['name']}"

            nested_metadata = {
                "group_label": self.looker_property["group_label"],
            }

            self.nested_dimensions = parse_all_fields(
                self.input_schema["fields"],
                None,
                is_repeated_field,
                nested_metadata,
            )

            self.looker_property["nested_properties"] = {
                "is_own_view": is_repeated_field,
                "view_name": self.looker_property["name"],
                "dimensions": self.nested_dimensions,
            }

    def as_dict(self):

        # Remove properties from self that are none
        for key, value in list(self.looker_property.items()):
            if value is None:
                del self.looker_property[key]

        return self.looker_property


def parse_all_fields(fields, primary_key, nested_mode=False, nested_metadata=None):
    parsed_fields = []
    for field in fields:
        response = Dimension(field, primary_key, nested_mode, nested_metadata).as_dict()
        parsed_fields.append(response)

        if response.get("nested_properties") is not None:
            if response["nested_properties"]["is_own_view"] == False:
                parsed_fields.extend(response["nested_properties"]["dimensions"])
                del response["nested_properties"]

    if len(parsed_fields) == 0:
        raise AssertionError("No fields parsed?")

    return parsed_fields
