"""Math helper functions for cross-type operations."""

import math
import cmath
from typing import Union

Numeric = Union[int, float, complex]


def safe_power(base: Numeric, exp: Numeric) -> Numeric:
    """
    Compute base^exp, handling edge cases for complex results.

    For negative bases with fractional exponents, returns complex.
    """
    if isinstance(base, complex) or isinstance(exp, complex):
        return cmath.exp(exp * cmath.log(base))

    # Check for negative base with fractional exponent
    if base < 0 and not float(exp).is_integer():
        return cmath.exp(exp * cmath.log(complex(base)))

    return base ** exp


def is_close(a: Numeric, b: Numeric, rel_tol: float = 1e-9, abs_tol: float = 0.0) -> bool:
    """
    Check if two numbers are approximately equal.

    Works for int, float, and complex.
    """
    if isinstance(a, complex) or isinstance(b, complex):
        return abs(complex(a) - complex(b)) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def format_number(n: Numeric, precision: int = 10) -> str:
    """
    Format a number for display.

    - Integers displayed without decimal
    - Floats rounded to precision
    - Complex formatted as a + bi
    """
    if isinstance(n, complex):
        real_str = format_number(n.real, precision)
        imag = n.imag
        if imag == 0:
            return real_str
        imag_str = format_number(abs(imag), precision)
        if n.real == 0:
            return f"{'-' if imag < 0 else ''}{imag_str}i"
        sign = " + " if imag >= 0 else " - "
        return f"{real_str}{sign}{imag_str}i"

    if isinstance(n, float):
        if n.is_integer():
            return str(int(n))
        # Round to precision and strip trailing zeros
        formatted = f"{n:.{precision}g}"
        return formatted

    return str(n)
