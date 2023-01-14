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

    def fields_to_lookml(self, fields=None, nested=False):
        if nested:
            return fields
        return parse_all_fields(fields)

    def validate_view(self, view):
        print(view)
        for dim in view["dimensions"]:
            if dim["dimension"].get("metadata"):
                del dim["dimension"]["metadata"]
            if dim["dimension"]["type"] is None:
                del dim["dimension"]["type"]
            if dim.get("fields") is not None:
                del dim["dimension"]["fields"]

        return view

    def to_lookml(self, fields=None, view_name=None, nested: bool = False):

        views = []

        create_view = {
            "view_name": view_name or self.view_name,
        }
        if nested is False:
            create_view["sql_table_name"] = self.sql_reference

        fields = fields or self.fields
        dimensions = self.fields_to_lookml(fields, nested)

        create_view["dimensions"] = dimensions

        for dim in dimensions:
            d = dim["dimension"]
            if d.get("fields") is not None and d["metadata"].get("repeat_type") == "complex":
                data_fields = d["fields"]

                nested_view_name = self.view_name.lower() + "__" + d["name"]

                # result = self.generate_nested_views(data_fields, nested_view_name)

                # views.append(result)

        views.append(create_view)

        output = {"views": [self.validate_view(view) for view in views]}

        parsed_lookml = lkml.dump(output)

        print(parsed_lookml)

        return parsed_lookml

    def generate_nested_views(self, fields, view_name):
        result = self.to_lookml(fields, view_name, nested=True)
        return result
