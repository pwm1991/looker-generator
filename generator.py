import lkml
from text import create_view_name, build_sql_reference, pretty_print
from parse_columns import parse_all_fields


class GenerateView:
    def __init__(self, schema):
        self.reference = schema["table_name"]
        self.view_name = create_view_name(schema["table_name"])
        self.fields = schema["fields"]
        self.sql_reference = build_sql_reference(schema["tableReference"])

    def fields_to_lookml(self, fields=None):
        return parse_all_fields(fields)

    def to_lookml(self):

        views = []

        create_view = {
            "reference": self.reference,
            "view_name": self.view_name,
            "sql_table_name": self.sql_reference,
        }

        dimensions = self.fields_to_lookml(self.fields)
        create_view["dimensions"] = dimensions

        for dim in dimensions:
            if dim.get("nested_view") is not None:
                new_view = dim["nested_view"]
                del dim["nested_view"]

                new_view["view_name"] = f"{self.view_name}__{new_view['view_name']}".lower()

                views.append(new_view)

        views.append(create_view)

        views = views[::-1]

        pretty_print(views)
