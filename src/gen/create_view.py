from os import mkdir
import lkml
from src.gen.columns import parse_all_fields, clean_looker_properties
from src.gen.looker import looker_warning
from src.gen.text import quote_string


class View:
    def __init__(self, schema, is_nested_view=False, parent=None):
        self.is_nested = is_nested_view
        self.schema = schema
        self.parent = parent
        self.nested_fields = []
        self.root_view_settings()

    def root_view_settings(self):
        if self.is_nested is False:

            self.table_id = self.schema.id
            self.full_table_id = self.schema.full_table_id
            self.filename = self.schema.filename
            self.view_name = self.schema.parent_looker_reference
            self.fields = self.schema.fields
        else:
            self.view_name = self.schema["view_name"]
            self.parsed_fields = list(self.schema["dimensions"])

    def clean_dimensions(self):
        dims_to_clean = self.parsed_fields
        if self.is_nested is True:
            self.parse_fields = self.schema["dimensions"]
        self.parsed_fields = [
            clean_looker_properties(dim) for dim in dims_to_clean if dim is not None
        ]

    def parse_fields(self):
        self.parsed_fields = parse_all_fields(self.fields, self.schema.primary_key)

    def get_parent_view_name(self):
        return self.table_id

    def get_dimensions(self):
        return self.parsed_fields

    def _translate_fields_to_types(self):
        supported_types = ["dimension", "dimension_group", "measure"]
        results = {}
        for type in supported_types:
            results[type] = []
            for field in self.parsed_fields:
                if field.get("field_type") == type:
                    del field["field_type"]
                    results[type].append(field)
            if len(results[type]) == 0:
                del results[type]

        if results == {}:
            raise Exception("No fields found for view")

        return results

    def to_dict(self):
        view = dict()
        fields = self._translate_fields_to_types()
        if self.is_nested is False:
            view.update(
                {
                    "name": self.schema.parent_looker_reference,
                    "sql_table_name": quote_string(self.full_table_id),
                    "view_name": self.schema.pretty_name,
                }
            )
        else:
            view.update({"name": f"{self.parent}__{self.view_name}__raw"})
        view.update(fields)
        return view


class GenerateView:
    def __init__(self, schema):
        self.schema = schema
        self.fields = schema.fields

    def prepare_looker_for_write(self, lookml_input):
        total_views = len(lookml_input["views"])

        print("Total views to create in file:", total_views)

        return looker_warning(total_views) + (lkml.dump(lookml_input) or "")

    def save_file(self, data):
        path_to_write = f".coverage/{self.schema.filename}"

        # create directory ./coverage if it doesn't exist
        try:
            mkdir(".coverage")
        except FileExistsError:
            pass

        with open(path_to_write, "w") as f:

            f.write(data)
            print(f"Wrote LookML to file: ", path_to_write)

    def handle_nested_views(self, dim):
        views = []

        if dim.get("nested_view") is None:
            return
        view = View(dim["nested_view"], is_nested_view=True, parent=self)
        view.clean_dimensions()

        print("Processing view", dim["name"])

        views.append(view.to_dict())

        for dim in view.parsed_fields:
            if dim.get("nested_view") is not None:
                view = self.handle_nested_views(dim)

                del dim["nested_view"]
                del dim["dimensions"]

                if view is not None:
                    # merge arrays
                    views = views + view

        return views

    def to_lookml(self):

        views = []

        view = View(self.schema)

        view.parse_fields()
        view.clean_dimensions()

        # filter only nested_views
        fields_with_nested_views = [
            dim for dim in view.parsed_fields if dim.get("nested_view") is not None
        ]
        for dim in fields_with_nested_views:

            nested_views = self.handle_nested_views(dim)

            if nested_views is not None:
                views = views + nested_views

        # For each dim in a view, run it through clean_looker_properties and create a new array
        for dim in view.parsed_fields:
            # replace dim with cleaned version
            view.parsed_fields[view.parsed_fields.index(dim)] = clean_looker_properties(
                dim
            )

        views.append(view.to_dict())

        # Reverse so root view is at the top
        if len(views) > 1:
            views = views[::-1]
            unified_view_name = views[0]["name"]
            for view in views:
                if view["name"] != unified_view_name:
                    view["name"] = unified_view_name

        lookml_to_generate = {"views": views}

        parsed = self.prepare_looker_for_write(lookml_to_generate)

        # save parsed output to file
        self.save_file(parsed)
