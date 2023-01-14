import lkml
from text import create_view_name, build_sql_reference
from parse_columns import parse_all_fields


class GenerateView:
    def __init__(self, schema):
        self.view_name = create_view_name(schema["table_name"])
        self.fields = schema["fields"]
        self.sql_reference = build_sql_reference(
            schema["table_catalog"], schema["table_schema"], schema["table_name"]
        )

    def to_lookml(self, sql_reference=None, view_name=None, fields=None):

        views = []

        create_view = {
            "sql_table_name": sql_reference or self.sql_reference,
            "view_name": view_name or self.view_name,
        }

        fields = fields or self.fields

        dimensions = parse_all_fields(fields)

        if len(dimensions) == 0 or dimensions is None:
            raise AssertionError("No fields parsed")
        else:
            create_view["dimensions"] = dimensions

        for dim in dimensions:
            if dim.get("fields") is not None and dim["metadata"]["repeat_type"] == "complex":
                dim_fields = dim["fields"]
                result = self.generate_nested_views(dim_fields)
                views.append(result)

        views.append(create_view)

        output = {"views": views}

        parsed_lookml = lkml.dump(output)

        print(parsed_lookml)

        return parsed_lookml

    def generate_nested_views(self, fields):
        return self.to_lookml(fields, "test", "test")
