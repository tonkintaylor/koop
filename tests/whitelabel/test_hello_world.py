"""Tests for the hello_world function."""

from whitelabel.functions.hello_world import hello_world


def test_hello_world():
    """Test hello_world function returns expected greeting."""
    result = hello_world("World")
    assert result == "Hello, World!"
