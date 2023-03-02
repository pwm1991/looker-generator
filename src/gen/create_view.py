from os import mkdir
import os
import lkml
from src.gen.columns import parse_all_fields
from src.gen.looker import looker_file_disclaimer, filter_invalid_looker_properties
from src.gen.text import backtick_string
import src.gen.errors as e

from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIRECTORY = (os.getenv("OUTPUT_DIRECTORY") or "").replace("/", "")


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
            self.schema_fields = self.schema.fields

    def parse_fields(self):
        self.parsed_fields = parse_all_fields(
            self.schema_fields, self.schema.primary_key
        )

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
                    field = filter_invalid_looker_properties(field)
                    results[type].append(field)
            if len(results[type]) == 0:
                del results[type]

        if results == {}:
            raise e.ViewHasNoFieldsException

        return results

    def to_dict(self):
        view = dict()
        fields = self._translate_fields_to_types()

        if self.is_nested is False:
            view.update(
                {
                    "name": self.schema.parent_looker_reference,
                    "sql_table_name": backtick_string(self.full_table_id),
                    "label": self.schema.pretty_name,
                }
            )
        view.update(fields)
        return view


class RepeatedView(View):
    def __init__(self, schema, parent):
        self.schema = schema
        self.parent = parent
        self.view_name = parent.parent_looker_reference + "__" + schema["name"]
        self.parsed_fields = schema["nested_properties"]["dimensions"]
        self.label = parent.pretty_name

    def to_dict(self):

        view = dict()

        fields = self._translate_fields_to_types()

        view.update(
            {
                "name": self.view_name,
                "label": self.label,
            }
        )
        view.update(fields)
        return view


class GenerateView:
    def __init__(self, schema):
        self.schema = schema
        self.fields = schema.fields

    def prepare_looker_for_write(self, lookml_input):
        total_views = len(lookml_input["views"])

        print("Total views to create in file:", total_views)

        lkml_output = lkml.dump(lookml_input) or ""

        return looker_file_disclaimer(total_views) + lkml_output

    # TODO: replace this with the looker API.
    def save_file(self, data):
        path_to_write = f"./{OUTPUT_DIRECTORY}/{self.schema.filename}"

        # create directory ./{OUTPUT_DIRECTORY} if it doesn't exist
        try:
            mkdir(f"./{OUTPUT_DIRECTORY}")
        except FileExistsError:
            pass

        with open(path_to_write, "w") as f:

            f.write(data)
            print(f"Wrote LookML to file: ", path_to_write)

    def handle_nested_views(self, nested_view):
        views = []

        # if nesed view nested properties dimensions is None, raise exception
        if nested_view["nested_properties"]["dimensions"] is None:
            raise e.NestedViewHasNoDimensionsException

        view = RepeatedView(nested_view, parent=self.schema).to_dict()

        views.append(view)
        if view.get("parsed_fields") is not None:
            for nested_view in view["parsed_fields"]:
                if nested_view.get("nested_view") is not None:
                    view = self.handle_nested_views(nested_view)

                    del nested_view["nested_properties"]

                    if view is not None:
                        # merge arrays
                        views = views + view

        return views

    def to_lookml(self):

        views = []

        view = View(self.schema)

        view.parse_fields()

        # filter only nested_views
        fields_with_nested_views = []
        for dim in view.parsed_fields:
            if dim.get("nested_properties") is not None:
                fields_with_nested_views.append(dim)

        for dim in fields_with_nested_views:

            print("Processing nested view", dim["name"])

            nested_views = self.handle_nested_views(dim)

            if nested_views is not None:
                views = views + nested_views

        views.append(view.to_dict())

        # Reverse so root view is at the top
        if len(views) > 1:
            views = views[::-1]
            unified_view_name = views[0]["label"]
            # Set the name of all views to the root view name so that they group together in the sidebar.
            for view in views:
                view["label"] = unified_view_name

        lookml_to_generate = {"views": views}

        parsed = self.prepare_looker_for_write(lookml_to_generate)

        # save parsed output to file
        self.save_file(parsed)
