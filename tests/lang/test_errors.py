"""Tests for the lang/errors module."""

import pytest
from mathlang.lang.errors import MathLangError, ParseError, SyntaxError


class TestMathLangError:
    """Tests for the base MathLangError."""

    def test_basic_error(self):
        error = MathLangError("test error")
        assert str(error) == "test error"

    def test_is_exception(self):
        assert issubclass(MathLangError, Exception)


class TestParseError:
    """Tests for ParseError."""

    def test_message_only(self):
        error = ParseError("unexpected token")
        assert "Parse error" in str(error)
        assert "unexpected token" in str(error)

    def test_with_line(self):
        error = ParseError("unexpected token", line=5)
        assert "line 5" in str(error)
        assert "unexpected token" in str(error)

    def test_with_line_and_column(self):
        error = ParseError("unexpected token", line=5, column=10)
        assert "line 5" in str(error)
        assert "column 10" in str(error)
        assert "unexpected token" in str(error)

    def test_line_property(self):
        error = ParseError("test", line=5, column=10)
        assert error.line == 5

    def test_column_property(self):
        error = ParseError("test", line=5, column=10)
        assert error.column == 10

    def test_inherits_from_mathlang_error(self):
        assert issubclass(ParseError, MathLangError)


class TestSyntaxError:
    """Tests for SyntaxError."""

    def test_inherits_from_parse_error(self):
        assert issubclass(SyntaxError, ParseError)

    def test_with_location(self):
        error = SyntaxError("invalid expression", line=3, column=7)
        assert "line 3" in str(error)
        assert "column 7" in str(error)
        assert "invalid expression" in str(error)
