import text

# create unittest for pretty_label
def test_pretty_label():
    assert text.pretty_label("test-test_test") == "Test Test Test"
    assert text.pretty_label("test_id") == "Test ID"
    assert text.pretty_label("test_pk") == "Test PK"
    assert text.pretty_label("test_tstamp") == "Test"


# create unittest for clean_view_name
def test_clean_view_name():
    assert text.clean_view_name("av_test") == "test"
    assert text.clean_view_name("test_av") == "test"
    assert text.clean_view_name("test_av_test") == "test_test"


# create unittest for build_sql_reference
def test_build_sql_reference():
    assert (
        text.build_sql_reference(
            {
                "projectId": "testProject",
                "datasetId": "testDataset",
                "tableId": "testTable",
            }
        )
        == "testProject.testDataset.testTable"
    )


# create unittest for create_view_name
def test_create_view_name():
    assert text.create_view_name("av_test") == "Test"
    assert text.create_view_name("test_av") == "Test"
    assert text.create_view_name("test_av_test") == "Test Test"
    assert text.create_view_name("test_av_test_av") == "Test Test"
    assert text.create_view_name("test_av_test_av_test") == "Test Test Test"
