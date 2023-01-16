from src.gen.text import pretty_label
from src.gen.looker_utils import (
    bigquery_type_to_looker,
    looker_timeframes,
    bool_to_string,
)


def clean_looker_properties_timeframes(type, data_type):
    if data_type in ["DATE"]:
        # remove time from timeframes
        times = looker_timeframes
        times.remove("time")
        times.remove("raw")
        return times
    elif type == "time":
        return looker_timeframes


class Dimension:
    def __init__(self, dim, nested_mode=False):
        self.dim = dim
        self.nested_mode = nested_mode
        self.sql = self._set_sql_name()
        self.field_type = "dimension"
        self.name = dim["column_name"].lower()
        self.type = bigquery_type_to_looker(dim["data_type"])
        self.description = dim.get("description") or None
        self.label = pretty_label(dim["column_name"])
        self.group_label = self._set_group_label()
        self.column_default = self._set_column_default()
        self.primary_key = self._guess_primary_key()

    def _set_sql_name(self):
        if self.nested_mode == False:
            return f"${{TABLE}}.{self.dim['column_name']}"
        else:
            return self.dim["column_name"]

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

    def _guess_primary_key(self):
        # check if name is in a list of primary keys
        if self.name in ["id", "primary_key", "pk"]:
            return bool_to_string(True)

    def _set_time(self):
        self.timeframes = (
            clean_looker_properties_timeframes(self.type, self.dim["data_type"]) or None
        )
        if self.timeframes is not None:
            self.field_type = "dimension_group"
            # Never convert the timezone for timeframes
            self.convert_tz = "no"

    def handle_repeated_fields(self):
        if self.dim["data_type"] not in ["RECORD", "REPEATED"]:
            return
        self.hidden = "yes"
        del self.type

        if self.dim.get("fields") is not None:
            self.dimensions = parse_all_fields(self.dim["fields"], True)

            # add group_label key to each dimension in dimensions
            self.group_label = pretty_label(self.name)

            self.nested_view = {
                "view_name": self.name,
                "dimensions": self.dimensions,
            }

    def as_dict(self):
        self._set_time()
        self.handle_repeated_fields()
        return self.__dict__

    def clean_looker_properties(self):
        o = self.as_dict()

        invalid_keys = [
            "dim",
            "nested_mode",
        ]
        # Remove keys where value is none
        output = {k: v for k, v in o.items() if v is not None}

        # Remove keys that are not valid in Looker

        # Remove keys that are in keys_to_remove
        output = {k: v for k, v in output.items() if k not in invalid_keys}

        return output


def parse_all_fields(fields, nested_mode=False):
    parsed_fields = []
    for field in fields:
        response = Dimension(field, nested_mode)
        parsed_fields.append(response)

    if len(parsed_fields) == 0:
        raise AssertionError("No fields parsed?")

    return parsed_fields
