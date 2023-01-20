from src.gen.text import convert_to_snake_case


def validate_table_reference(reference):
    if len(reference.split(".")) != 3:
        return False


class BigQueryTableReference:
    def __init__(self, table_reference, view_metadata):
        self.id = table_reference.table_id
        self.full_table_id = table_reference.full_table_id
        self.fields = table_reference._properties["schema"]["fields"]
        self.parent_looker_reference = self._create_looker_reference()
        self.filename = self._create_filename()
        self.pretty_name = view_metadata["name"]
        self.primary_key = view_metadata["primary_key"] or None

    def _create_looker_reference(self):
        string = self.id
        for l in ["_av", "av_", "_vw", "vw_"]:
            string = string.replace(l, "")
        return (string + "__raw").lower()

    def _create_filename(self):
        filename = self.id
        filename = convert_to_snake_case(filename)
        filename = filename.lower()
        return filename + ".raw.view.lkml"

    def to_dict(self):
        return self
