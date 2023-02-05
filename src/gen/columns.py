from src.gen.text import gen_field_label
from src.gen.looker import (
    bigquery_type_to_looker_type,
    looker_timeframes,
    bool_to_string,
)


def clean_looker_property_timeframes(looker_type, data_type):
    if data_type in ["DATE"]:
        # remove time from timeframes
        times = looker_timeframes
        times.remove("time")
        times.remove("raw")
        return times
    elif looker_type == "time":
        return looker_timeframes


def clean_looker_properties(self):

    # if self has __dict__ attribute, use that
    if hasattr(self, "__dict__"):
        self = self.__dict__

    # Keep field_type here so that it can be sorted later
    invalid_keys = ["dim", "nested_mode", "nested_view", "dimensions", "name"]

    # Remove keys where value is none
    output = {k: v for k, v in self.items() if v is not None}

    # Remove keys that are in keys_to_remove, valid in Looker.
    # TODO: Consider making this a positive opt-in? I.e. only supported keys are allowed.
    output = {k: v for k, v in output.items() if k not in invalid_keys}

    return output


class Dimension:
    def __init__(self, dim, primary_key, nested_mode=False):
        self.dim = dim
        self.primary_key = primary_key or None
        self.nested_mode = nested_mode
        self.sql = self._set_sql_name()
        self.field_type = "dimension"
        self.name = dim["name"].lower()
        self.type = bigquery_type_to_looker_type(dim["type"])
        self.description = dim.get("description") or None
        self.label = gen_field_label(dim["name"])
        self.group_label = self._set_group_label()
        self.column_default = self._set_column_default()
        self.primary_key = self._set_primary_key()

    def _set_sql_name(self):
        if self.nested_mode == False:
            return f"${{TABLE}}.{self.dim['name']}"
        else:
            return self.dim["name"]

    def _set_group_label(self):
        diagnostic_fields = ["event_id", "run_id"]
        snowplow_identifiers = [
            "session_id",
            "network_userid",
            "domain_sessionid",
            "user_id",
        ]
        if self.name in diagnostic_fields:
            return "Diagnostic Fields"
        elif self.name in snowplow_identifiers:
            return "Snowplow Identifiers"

    def _set_column_default(self):
        if self.dim.get("COLUMN_DEFAULT") is not None:
            return self.dim["COLUMN_DEFAULT"]

    def _set_primary_key(self):
        # check if name is in a list of primary keys
        if self.primary_key == self.name:
            return bool_to_string(True)

    def _set_time(self):
        self.timeframes = (
            clean_looker_property_timeframes(self.type, self.dim["type"]) or None
        )
        if self.timeframes is not None:
            self.field_type = "dimension_group"
            # Never convert the timezone for timeframes
            self.convert_tz = "no"

    def handle_repeated_fields(self):
        if self.dim["type"] not in ["RECORD"]:
            return

        repeated_field_nested_mode = False
        if self.dim.get("mode") in ["REPEATED"]:
            self.hidden = "yes"
            repeated_field_nested_mode = True
            del self.type

        fields = self.dim.get("fields")
        if fields is not None:
            if repeated_field_nested_mode == False:
                # For nested, non-repeating fields, prepend the parent dim.name
                for field in fields:
                    field["name"] = f"{self.dim['name']}.{field['name']}"

            self.dimensions = parse_all_fields(
                self.dim["fields"],
                nested_mode=repeated_field_nested_mode,
                primary_key=None,
            )

            # add group_label key to each dimension in dimensions
            self.group_label = gen_field_label(self.name)

            self.nested_view = {
                "view_name": self.name,
                "dimensions": self.dimensions,
            }

    def as_dict(self):
        self._set_time()
        self.handle_repeated_fields()
        return self.__dict__


def parse_all_fields(fields, primary_key, nested_mode=False):
    parsed_fields = []
    for field in fields:
        response = Dimension(field, primary_key, nested_mode)
        parsed_fields.append(response)

    if len(parsed_fields) == 0:
        raise AssertionError("No fields parsed?")

    return parsed_fields
