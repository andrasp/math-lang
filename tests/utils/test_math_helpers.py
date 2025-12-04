"""Tests for math helper functions."""

import math
import cmath
import pytest

from mathlang.utils.math_helpers import safe_power, is_close, format_number


class TestSafePower:
    """Tests for safe_power function."""

    def test_integer_power(self):
        assert safe_power(2, 3) == 8

    def test_float_power(self):
        assert safe_power(2.0, 3.0) == pytest.approx(8.0)

    def test_fractional_power(self):
        assert safe_power(4, 0.5) == pytest.approx(2.0)

    def test_negative_base_integer_exponent(self):
        assert safe_power(-2, 3) == -8

    def test_negative_base_fractional_exponent(self):
        result = safe_power(-1, 0.5)
        assert isinstance(result, complex)
        assert abs(result - 1j) < 1e-10

    def test_complex_base(self):
        result = safe_power(1j, 2)
        assert is_close(result, -1)

    def test_complex_exponent(self):
        result = safe_power(2, 1j)
        assert isinstance(result, complex)

    def test_zero_base_positive_exp(self):
        assert safe_power(0, 2) == 0

    def test_any_base_zero_exp(self):
        assert safe_power(5, 0) == 1


class TestIsClose:
    """Tests for is_close function."""

    def test_equal_integers(self):
        assert is_close(5, 5)

    def test_close_floats(self):
        assert is_close(1.0, 1.0 + 1e-12)

    def test_not_close_floats(self):
        assert not is_close(1.0, 1.1)

    def test_close_with_abs_tol(self):
        assert is_close(0.0, 1e-12, abs_tol=1e-10)

    def test_not_close_with_abs_tol(self):
        assert not is_close(0.0, 1e-8, abs_tol=1e-10)

    def test_close_complex(self):
        assert is_close(1+1j, 1+1j+1e-12j)

    def test_not_close_complex(self):
        assert not is_close(1+1j, 1+2j)

    def test_mixed_types(self):
        assert is_close(1, 1.0)


class TestFormatNumber:
    """Tests for format_number function."""

    def test_integer(self):
        assert format_number(42) == "42"

    def test_negative_integer(self):
        assert format_number(-10) == "-10"

    def test_float_with_decimal(self):
        assert format_number(3.14159) == "3.14159"

    def test_float_as_integer(self):
        assert format_number(5.0) == "5"

    def test_complex_both_parts(self):
        assert format_number(3+4j) == "3 + 4i"

    def test_complex_negative_imag(self):
        assert format_number(3-4j) == "3 - 4i"

    def test_complex_only_real(self):
        assert format_number(5+0j) == "5"

    def test_complex_only_imag(self):
        assert format_number(0+4j) == "4i"

    def test_complex_negative_only_imag(self):
        assert format_number(0-4j) == "-4i"

    def test_precision(self):
        result = format_number(1.23456789012345, precision=5)
        assert len(result) <= 7

    def test_very_small_float(self):
        result = format_number(1e-15)
        assert "e" in result.lower() or result == "0"

    def test_very_large_float(self):
        result = format_number(1e15)
        assert "e" in result.lower() or "1000000000000000" in result
