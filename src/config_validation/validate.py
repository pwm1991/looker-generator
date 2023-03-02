unique_references = []


def validate_bigquery_ref(name):
    name = name.lower()
    if " " in name:
        return False
    if name == "":
        return False
    return True


def config_has_unsupported_props(properties):
    supported_properties = [
        "name",
        "description",
        "reference",
        "primary_key",
    ]
    invalid_properties = [
        property for property in properties if property not in supported_properties
    ]

    if len(invalid_properties) > 0:
        return True
    return False


def validate_config(config, BIGQUERY_PROJECT):
    errors = []

    # Tests whether the references are correct
    # split config[reference] by . and check that it has 3 parts

    if len(config["reference"].split(".")) != 3:
        errors.append("Reference must be in the format `project.dataset.table`")
    if not config["reference"].startswith(BIGQUERY_PROJECT):
        errors.append(f"Reference must start with {BIGQUERY_PROJECT}")

    # Tests if the primary key is valid
    if config.get("primary_key"):
        is_valid = validate_bigquery_ref(config["primary_key"])
        if not is_valid:
            errors.append("Primary key isn't in a valid format")

    # Test if there are any unsupported properties
    if config_has_unsupported_props(config.keys()):
        errors.append("Unsupported properties found - these won't do anything!")

    return errors


def notify_mode(mode):
    valid_modes = ["RAISE", "SKIP", None]

    if mode not in valid_modes:
        raise Exception(
            f"Invalid mode: {mode}. Valid modes are: {','.join(valid_modes)}"
        )

    if mode == "RAISE":
        print("Mode is set to RAISE. Invalid views will stop the process")
    elif mode == "SKIP":
        print("Mode is set to SKIP. Invalid views will be skipped")
    elif mode == None:
        mode = "SKIP"
        print("Mode not specified. Defaulting to SKIP. Invalid views will be skipped")

    return mode


def validate_configs(BIGQUERY_PROJECT, configs, mode):

    mode = notify_mode(mode)

    valid_configs = {"valid": [], "invalid": [], "skipped": []}

    for config in configs:
        if config["reference"] in unique_references:
            raise Exception(f"Duplicate reference found: {config['reference']}")
        unique_references.append(config["reference"])

        errors = validate_config(config, BIGQUERY_PROJECT)

        if config.get("disabled"):
            print(f"Skipping {config['reference']}")
            valid_configs["skipped"].append(config)
            continue

        if len(errors) > 0:
            print(f"Found {len(errors)} errors in {config['reference']}")
            print(", ".join(errors))
            if mode == "RAISE":
                raise Exception(f"Invalid view: {config['reference']}")
            elif mode == "SKIP":
                print(f"Skipping {config['reference']}")
                valid_configs["invalid"].append(config)
        elif len(errors) == 0:
            valid_configs["valid"].append(config)

    return valid_configs["valid"]
