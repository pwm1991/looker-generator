from os import mkdir
import lkml
from src.gen.looker_utils import looker_warning
from src.gen.tests.text import (
    create_view_name,
    build_sql_reference,
    safe_filename,
    looker_reference,
)
from src.gen.columns import parse_all_fields


class View:
    def __init__(self, schema, nested=False, parent=None):
        self.nested = nested
        self.schema = schema
        self.parent = parent
        self.description = schema.get("description")
        self.nested_fields = []
        self.root_view_settings()

    def root_view_settings(self):
        if self.nested is False:

            self.table_id = self.schema["tableReference"]["tableId"]
            self.sql_reference = build_sql_reference(self.schema["tableReference"])
            self.filename = safe_filename(self.table_id)
            self.view_name = create_view_name(self.table_id)
            self.fields = self.schema.get("fields")
        else:
            self.view_name = create_view_name(
                f"{self.parent}__{self.schema['view_name']}"
            )
            self.parsed_fields = list(self.schema["dimensions"])

    def clean_dimensions(self):
        dims_to_clean = self.parsed_fields
        if self.nested is True:
            self.parse_fields = self.schema["dimensions"]
        self.parsed_fields = [
            dim.clean_looker_properties() for dim in dims_to_clean if dim is not None
        ]

    def remove_nested_dim(self, dim_name):
        for dim in self.parsed_fields:
            if dim_name == dim["name"]:
                del dim["nested_view"]
                del dim["dimensions"]

    def parse_fields(self):
        self.parsed_fields = parse_all_fields(self.fields)

    def get_parent_view_name(self):
        return self.table_id

    def get_dimensions(self):
        return self.parsed_fields

    def to_dict(self):
        view = dict()
        if self.nested is False:
            view.update(
                {
                    "name": looker_reference(self.table_id),
                    "sql_table_name": self.sql_reference,
                    "view_name": self.view_name,
                    "description": self.description or "",
                }
            )
        else:
            view.update(
                {
                    "name": looker_reference(
                        f"{self.parent}__{self.schema['view_name']}"
                    ),
                }
            )

        # merge two objects
        view.update(
            {
                "view_name": self.view_name,
                "dimensions": self.parsed_fields,
            }
        )
        return view


class GenerateView:
    def __init__(self, schema):
        self.schema = schema
        self.file_name = safe_filename(schema["tableReference"]["tableId"])
        self.fields = schema["fields"]

    def prepare_looker_for_write(self, lookml_input):
        total_views = len(lookml_input["views"])

        print("Total views to create in file:", total_views)

        return looker_warning(total_views) + (lkml.dump(lookml_input) or "")

    def save_file(self, data):
        path_to_write = f".coverage/{self.file_name}"

        # create directory ./coverage if it doesn't exist
        try:
            mkdir(".coverage")
        except FileExistsError:
            pass

        with open(path_to_write, "w") as f:

            f.write(data)
            print(f"Wrote LookML to file: ", path_to_write)

    def handle_nested_views(self, dim, parent_view_name):
        views = []

        if dim.get("nested_view") is None:
            return
        view = View(dim["nested_view"], nested=True, parent=parent_view_name)
        view.clean_dimensions()

        print("Processing view", dim["name"])

        views.append(view.to_dict())

        # for dim in view["dimensions"]:
        #     if dim.get("nested_view") is not None:
        #         view = self.handle_nested_views(dim)

        #         del dim["nested_view"]
        #         del dim["dimensions"]

        #         if view is not None:
        #             # merge arrays

        #             views = views + view

        return views

    def to_lookml(self):

        views = []

        view = View(self.schema)

        view.parse_fields()
        view.clean_dimensions()

        parent_view_name = view.get_parent_view_name()

        for dim in view.parsed_fields:

            if dim.get("nested_view") is not None:

                nested_views = self.handle_nested_views(dim, parent_view_name)

                view.remove_nested_dim(dim["name"])

                if nested_views is not None:
                    views = views + nested_views

        views.append(view.to_dict())

        # Reverse so root view is at the top
        views = views[::-1]

        lookml_to_generate = {"views": views}

        parsed = self.prepare_looker_for_write(lookml_to_generate)

        # save parsed output to file
        self.save_file(parsed)
