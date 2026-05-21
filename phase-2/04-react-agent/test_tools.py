import pytest

from tools import calculator, execute_tool, lookup


def test_calculator_returns_string_for_integer_math():
    assert calculator("15 * 7") == "105"


def test_calculator_returns_int_string_for_clean_float():
    assert calculator("10/2") == "5"


def test_calculator_raises_on_invalid_input():
    with pytest.raises(Exception):
        calculator("not a calc str")


def test_lookup_returns_fact_for_lowercase_key():
    assert lookup("capital of australia") == "Canberra"


def test_lookup_returns_fact_for_mixed_casing():
    assert lookup("Capital of Australia") == "Canberra"


def test_lookup_returns_fact_with_whitespace():
    assert lookup("   capital of australia   ") == "Canberra"


def test_lookup_returns_not_found_for_unknown_key():
    assert (
        lookup("Something you cant look up")
        == "No information found for: Something you cant look up"
    )


def test_lookup_preserves_original_casing_in_error():
    result = lookup("Capital of Mars")
    assert result == "No information found for: Capital of Mars"


def test_execute_tool_happy_path():
    assert execute_tool("calculator", "5+11") == "16"


def test_execute_tool_returns_error_for_unknown_tool():
    assert (
        execute_tool("not a tool", "args")
        == "Unknown tool 'not a tool'. Available: calculator, lookup"
    )


def test_execute_tool_catches_tool_exception():
    """When a tool raises, execute_tool converts the exception to an error string."""
    result = execute_tool("calculator", "cannot be calculated")
    assert result.startswith("Tool error:")
