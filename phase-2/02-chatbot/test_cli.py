from cli import validate_input


def test_input_too_short():
    assert not validate_input("a")


def test_input_too_long():
    assert not validate_input("a" * 2001)


def test_validate_input():
    assert validate_input("Good string length")
