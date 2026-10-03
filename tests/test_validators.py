import pytest

from services.validators import clean_name, is_valid_email


@pytest.mark.parametrize("value", ["a@b.com", "first.last+tag@mail.example.co.in", " me@x.org "])
def test_valid_emails(value):
    assert is_valid_email(value)


@pytest.mark.parametrize("value", ["", "no-at-sign", "a@b", "a@@b.com", "a b@c.com", "a@b.com\nBcc: x@y.com"])
def test_invalid_emails(value):
    assert not is_valid_email(value)


def test_clean_name_collapses_whitespace_and_caps_length():
    assert clean_name("  Ravi \n  Kumar ") == "Ravi Kumar"
    assert len(clean_name("x" * 500)) == 60
