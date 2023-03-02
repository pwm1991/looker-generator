import validate as v


def test_validate_bigquery_ref():
    def test_has_no_spaces():
        input_string = "hello world"
        assert v.validate_bigquery_ref(input_string) == False

    def test_is_not_empty():
        input_string = ""
        assert v.validate_bigquery_ref("") == False

    def test_is_valid_string():
        input_string = "hello_world"
        assert v.validate_bigquery_ref(input_string) == True

    test_has_no_spaces()
    test_is_not_empty()
    test_is_valid_string()


def test_config_has_unsupported_props():
    def test_has_unsupported_props():
        input_properties = ["foo"]
        assert v.config_has_unsupported_props(input_properties) == True

    def test_has_no_unsupported_props():
        input_properties = ["name"]
        assert v.config_has_unsupported_props(input_properties) == False

    test_has_unsupported_props()
    test_has_no_unsupported_props()


def test_validate_config():
    INPUT_BIGQUERY_PROJECT = "project"

    def test_a_valid_input():
        config = {
            "name": "example",
            "reference": "project.dataset.table",
            "primary_key": "id",
        }
        assert v.validate_config(config, INPUT_BIGQUERY_PROJECT) == []

    def test_invalid_config():
        config = {
            "name": "example",
            "reference": "dataset.table",
            "primary_key": "id that isn't valid",
        }
        result = v.validate_config(config, INPUT_BIGQUERY_PROJECT)
        print(result)
        assert len(result) > 0

    test_a_valid_input()
    test_invalid_config()
