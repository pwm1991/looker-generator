import src.gen.text as text

# create unittest for gen_field_label
def test_gen_field_label():
    assert text.gen_field_label("test-test_test") == "Test Test Test"
    assert text.gen_field_label("test_pk") == "Test PK"
    assert text.gen_field_label("test_id") == "Test ID"
    assert text.gen_field_label("test_tstamp") == "Test"


# create unittest for convert_to_string_case
def test_convert_to_string_case():
    assert text.convert_to_string_case("test-test_test") == "test test test"
    assert text.convert_to_string_case("test_id") == "test id"
    assert text.convert_to_string_case("test-pk") == "test pk"
    assert text.convert_to_string_case("test_tstamp") == "test tstamp"
