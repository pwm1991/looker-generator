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

    assert dimension == {
        "name": "example_repeated",
        "label": "Example Repeated",
        "field_type": "dimension",
        "sql": "${TABLE}.example_repeated",
        "hidden": "yes",
        "nested_properties": {
            "is_own_view": True,
            "view_name": "example_repeated",
            "dimensions": [
                {
                    "name": "segment_name",
                    "sql": "segment_name",
                    "label": "Segment Name",
                    "type": "string",
                    "field_type": "dimension",
                }
            ],
        },
    }


def test_record_non_repeated():
    nested_mode = False
    input_schema = {
        "name": "app",
        "type": "RECORD",
        "fields": [
            {"name": "app__name", "type": "STRING", "sql": "app.name"},
            {"name": "app__version", "type": "STRING", "sql": "app.version"},
            {"name": "app__build", "type": "STRING", "sql": "app.build"},
        ],
    }

    dimension = Dimension(input_schema, None, nested_mode).as_dict()

    assert dimension == {
        "is_own_view": False,
        "view_name": "app",
        "dimensions": [
            {
                "name": "app__name",
                "sql": "${TABLE}.app.name",
                "label": "App Name",
                "group_label": "App",
                "type": "string",
                "field_type": "dimension",
            },
            {
                "name": "app__version",
                "sql": "${TABLE}.app.version",
                "label": "App Version",
                "group_label": "App",
                "type": "string",
                "field_type": "dimension",
            },
            {
                "name": "app__build",
                "sql": "${TABLE}.app.build",
                "label": "App Build",
                "group_label": "App",
                "type": "string",
                "field_type": "dimension",
            },
        ],
    }
