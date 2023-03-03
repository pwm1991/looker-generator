from src.gen.measures import Measure, identify_value_format_name

example = {
    "name": "app__build",
    "sql": "${TABLE}.app.build",
    "label": "App Build",
    "group_label": "App",
    "description": "The build number of the app.",
    "type": "number",
    "field_type": "dimension",
}


def assert_fully_formed_dimension_to_measure():
    input = example
    m = Measure(input).measures()
    if len(m) > 0:
        output = m[0]
        output_to_test = output["type"]

        assert output["type"] == output_to_test
        assert output["name"] == f"m_app__build__${output_to_test}"
        assert output["label"] == f"App Build (${output_to_test})"
        assert (
            output["description"]
            == f"${example.get('description')} (${output_to_test})"
        )


def assert_dim_has_no_description():
    """When the dimension has no description, the measure should have a description based on the label"""
    input = example
    del input["description"]
    m = Measure(example).measures()
    if len(m) > 0:
        output = m[0]
        output_to_test = output["type"]

        assert output["description"] == f"{output_to_test} of {input['label']}"


def assert_identify_value_format_name():
    inputs = [
        {"input": "label_global", "output": "gbp"},
        {"input": "label_usd", "output": "usd"},
        {"input": "label_ratio", "output": "percent_2"},
        {"input": "label_percent", "output": "percent_2"},
        {"input": "label_pct", "output": "percent_2"},
        {"input": "label", "output": "decimal_2"},
    ]
    for input in inputs:
        assert identify_value_format_name(input["input"]) == input["output"]
