class ConfigHasDuplicateViewReferencesException(Exception):
    def __init__(self, view_name):
        super().__init__(
            f"The {view_name} has already been declared in the config file. Please remove the duplicate view_name {view_name}"
        )


class PrimaryKeyDeclaredButPointlessException(Exception):
    def __init__(self, view_name, primary_key):
        super().__init__(
            f"The {view_name} has a primary_key declared, but it's pointless. Received: '{primary_key}'"
        )


def validate_view_references(references: dict):
    # ensure no duplicate objects in array
    reference_names = []
    for ref in references:
        reference_name = ref["name"]
        if reference_name in reference_names:
            raise ConfigHasDuplicateViewReferencesException(reference_name)
        reference_names.append(reference_name)

    return True
