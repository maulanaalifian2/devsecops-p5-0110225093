from app.utils import parse_bool, sanitize_text, validate_description, validate_title


def test_validate_title_ok():
    assert validate_title("Judul valid") is None


def test_validate_title_empty_and_type():
    assert validate_title("   ") is not None
    assert validate_title(123) is not None


def test_validate_title_too_long():
    assert validate_title("x" * 101) is not None


def test_validate_description():
    assert validate_description("ok") is None
    assert validate_description("x" * 501) is not None
    assert validate_description(None) is not None


def test_sanitize_text_removes_control_chars():
    assert sanitize_text("  halo\x00dunia  ") == "halodunia"


def test_parse_bool():
    assert parse_bool("true") is True
    assert parse_bool("0") is False
    assert parse_bool("abc") is None
