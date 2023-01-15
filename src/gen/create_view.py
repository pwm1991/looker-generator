import lkml
from gen.looker_utils import looker_warning
from gen.tests.text import create_view_name, build_sql_reference, safe_filename
from gen.columns import parse_all_fields


class GenerateView:
    def __init__(self, schema):
        self.table_name = schema["tableReference"]["tableId"]
        self.reference = self.table_name
        self.view_name = create_view_name(self.table_name)
        self.fields = schema["fields"]
        self.sql_reference = build_sql_reference(schema["tableReference"])

    def fields_to_lookml(self, fields=None):
        return parse_all_fields(fields)

    def prepare_file_to_write(self, lookml):
        total_views = len(lookml["views"])

        print("Total views to create in file: ", total_views)

        output = looker_warning(total_views)
        return output + (lkml.dump(lookml) or "")

    def save_file(self, data):
        filename = f"{self.view_name}.view"
        filename = safe_filename(filename)
        path_to_write = f".coverage/{filename}"
        with open(path_to_write, "w") as f:

            f.write(data)
            print(f"Wrote LookML to file: ", path_to_write)

    def handle_nested_views(self, dim):
        views = []

        if dim.get("nested_view") is None:
            return
        new_view = dim["nested_view"]

        print("Processing view ", dim["name"])

        new_view["view_name"] = self.view_name
        new_view["name"] = f"{self.view_name}__{dim['name']}".lower()

        views.append(new_view)

        for dim in new_view["dimensions"]:
            if dim.get("nested_view") is not None:
                new_view = self.handle_nested_views(dim)

                del dim["nested_view"]

                if new_view is not None:
                    # merge arrays

                    views = views + new_view

        return views

    def to_lookml(self):

        views = []

        create_view = {
            "name": self.reference,
            "view_name": self.view_name,
            "sql_table_name": self.sql_reference,
        }

        dimensions = self.fields_to_lookml(self.fields)
        create_view["dimensions"] = dimensions

        for dim in dimensions:
            if dim.get("nested_view") is not None:

                nested_views = self.handle_nested_views(dim)

                del dim["nested_view"]

                if nested_views is not None:
                    views = views + nested_views

        # iterate through all keys in a json object and find nested views

        views.append(create_view)

        views = views[::-1]

        lookml_to_generate = {"views": views}

        parsed = self.prepare_file_to_write(lookml_to_generate)

        # save parsed output to file
        self.save_file(parsed)
