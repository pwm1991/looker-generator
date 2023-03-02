from src.gen.text import set_field_label, convert_to_string_case

# create unittest for gen_field_label
def test_gen_field_label():
    assert set_field_label("test-test_test") == "Test Test Test"
    assert set_field_label("test_pk") == "Test PK"
    assert set_field_label("test_id") == "Test ID"
    assert set_field_label("test_tstamp") == "Test"


# create unittest for convert_to_string_case
def test_convert_to_string_case():
    assert convert_to_string_case("test-test_test") == "test test test"
    assert convert_to_string_case("test_id") == "test id"
    assert convert_to_string_case("test-pk") == "test pk"
    assert convert_to_string_case("test_tstamp") == "test tstamp"
