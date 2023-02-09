import pytest
from src.api.validate_config import (
    validate_view_references,
    ConfigHasDuplicateViewReferencesException,
)

example_reference = "example.example"


def test_validate_config_returns_valid():
    example = [
        {"name": "example", "reference": example_reference},
        {"name": "example2", "reference": example_reference},
    ]

    assert validate_view_references(example) == True


def test_validate_config_throws_when_duplicate():
    example = [
        {"name": "example", "reference": example_reference},
        {"name": "example", "reference": example_reference},
    ]

    with pytest.raises(ConfigHasDuplicateViewReferencesException):
        validate_view_references(example)
