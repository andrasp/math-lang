"""Type coercion rules for numeric operations."""

from typing import Any

from mathlang.types.scalar import Scalar


def coerce_numeric(a: Any, b: Any) -> tuple[Any, Any]:
    """
    Coerce two numeric values to a common type for operations.

    Promotion order: int -> float -> complex
    """
    # Extract raw values from Scalars
    val_a = a.value if isinstance(a, Scalar) else a
    val_b = b.value if isinstance(b, Scalar) else b

    # If either is complex, promote both to complex
    if isinstance(val_a, complex) or isinstance(val_b, complex):
        return complex(val_a), complex(val_b)

    # If either is float, promote both to float
    if isinstance(val_a, float) or isinstance(val_b, float):
        return float(val_a), float(val_b)

    # Both are int (or bool, which is subclass of int)
    return val_a, val_b


def is_numeric(value: Any) -> bool:
    """Check if a value is numeric (int, float, complex, or Scalar containing those)."""
    if isinstance(value, Scalar):
        value = value.value
    return isinstance(value, (int, float, complex)) and not isinstance(value, bool)


def is_truthy(value: Any) -> bool:
    """Determine the truthiness of a MathLang value."""
    if isinstance(value, Scalar):
        val = value.value
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return val != 0
        if isinstance(val, complex):
            return val != 0j
        if isinstance(val, str):
            return len(val) > 0
    return bool(value)
