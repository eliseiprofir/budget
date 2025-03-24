from utils.strings import truncate


def test_generate_random_string():
    """Test truncate function."""
    assert truncate("Hello, World!", 10) == "Hello, ..."
    assert truncate("Short", 10) == "Short"
    assert truncate(None, 10) == ""
    assert truncate("", 10) == ""
