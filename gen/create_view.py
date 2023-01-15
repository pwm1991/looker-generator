import lkml
from gen.looker_utils import looker_warning
from gen.text import create_view_name, build_sql_reference
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
        output = looker_warning(total_views)
        # parse to lookml
        return output + lkml.dump(lookml)

    def save_file(self, data):
        filename = f"{self.view_name}.view.lkml".lower()
        path_to_write = f".coverage/{filename}"
        with open(path_to_write, "w") as f:

            f.write(data)
            print(f"Wrote LookML to file: ", path_to_write)

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
                new_view = dim["nested_view"]
                del dim["nested_view"]

                new_view["view_name"] = self.view_name
                new_view["name"] = f"{self.view_name}__{dim['name']}".lower()

                views.append(new_view)

        views.append(create_view)

        views = views[::-1]

        lookml_to_generate = {"views": views}

        parsed = self.prepare_file_to_write(lookml_to_generate)

        # save parsed output to file
        self.save_file(parsed)
