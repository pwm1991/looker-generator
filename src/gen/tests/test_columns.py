from src.gen.columns import Dimension


def test_date_datatype():
    primary_key = "day"
    nested_mode = False
    input_schema = {
        "name": "day",
        "type": "DATE",
        "description": "Blah blah blah",
    }

    dimension = Dimension(input_schema, primary_key, nested_mode).as_dict()

    assert dimension == {
        "name": "day",
        "sql": "${TABLE}.day",
        "description": "Blah blah blah",
        "label": "Day",
        "primary_key": "yes",
        "type": "time",
        "timeframes": ["date", "week", "month", "quarter", "year"],
        "field_type": "dimension_group",
        "convert_tz": "no",
    }


def test_other_time_datatypes():
    primary_key = "day"
    nested_mode = False
    input_schema = {
        "name": "day",
        "type": "TIMESTAMP",
        "description": "Date (UTC unless specified)",
    }

    dimension = Dimension(input_schema, primary_key, nested_mode).as_dict()

    assert dimension == {
        "name": "day",
        "sql": "${TABLE}.day",
        "description": "Date (UTC unless specified)",
        "label": "Day",
        "primary_key": "yes",
        "type": "time",
        "timeframes": ["raw", "time", "date", "week", "month", "quarter", "year"],
        "field_type": "dimension_group",
        "convert_tz": "no",
    }


def test_non_repeated_string():
    primary_key = "event_id"
    nested_mode = False
    input_schema = {"name": "event_id", "type": "STRING", "description": "Event ID"}

    dimension = Dimension(input_schema, primary_key, nested_mode).as_dict()

    assert dimension == {
        "name": "event_id",
        "sql": "${TABLE}.event_id",
        "description": "Event ID",
        "label": "Event ID",
        "primary_key": "yes",
        "type": "string",
        "field_type": "dimension",
        "group_label": "Diagnostic Fields",
    }


def test_string_abbreviation():
    primary_key = "some value"
    nested_mode = False
    input_schema = {"name": "id", "type": "STRING", "description": "Some Value"}

    dimension = Dimension(input_schema, primary_key, nested_mode).as_dict()

    assert dimension == {
        "name": "id",
        "sql": "${TABLE}.id",
        "description": "Some Value",
        "label": "ID",
        "type": "string",
        "field_type": "dimension",
    }


def test_repeated_view_parent():
    nested_mode = False
    input_schema = {
        "name": "example_repeated",
        "type": "RECORD",
        "mode": "REPEATED",
        "fields": [{"name": "segment_name", "type": "STRING"}],
    }

    dimension = Dimension(input_schema, None, nested_mode).as_dict()

    assert dimension["hidden"] == "yes"
    assert dimension["label"] == "Example Repeated"
    assert dimension["nested_properties"] == {
        "is_own_view": True,
        "view_name": "example_repeated",
        "dimensions": [
            {
                "name": "segment_name",
                "sql": "segment_name",
                "label": "Segment Name",
                "type": "string",
                "group_label": "Example Repeated",
                "field_type": "dimension",
            }
        ],
    }


def test_record_non_repeated():
    nested_mode = False
    input_schema = {
        "name": "app",
        "type": "RECORD",
        "fields": [
            {"name": "name", "type": "STRING", "sql": "app.name"},
            {"name": "version", "type": "STRING", "sql": "app.version"},
            {"name": "build", "type": "STRING", "sql": "app.build"},
        ],
    }

    dimension = Dimension(input_schema, None, nested_mode).as_dict()

    print(dimension)

    input = dimension["nested_properties"]

    assert input["is_own_view"] == False
    assert input["view_name"] == "app"
    assert len(input["dimensions"]) > 0
    first_dimension = input["dimensions"][0]
    assert first_dimension["name"] == "app__name"
    assert first_dimension["sql"] == "${TABLE}.app.name"
    assert first_dimension["label"] == "App Name"
    assert first_dimension["group_label"] == "App"
