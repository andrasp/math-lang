"""Scalar type for single values (int, float, complex, bool, str, datetime)."""

from datetime import datetime
from typing import Union

from mathlang.types.base import MathObject

ScalarValue = Union[int, float, complex, bool, str, datetime]


class Scalar(MathObject):
    """A single value of any fundamental type."""

    def __init__(self, value: ScalarValue):
        self._value = value

    @property
    def value(self) -> ScalarValue:
        return self._value

    @property
    def type_name(self) -> str:
        if isinstance(self._value, bool):
            return "Boolean"
        elif isinstance(self._value, int):
            return "Integer"
        elif isinstance(self._value, float):
            return "Float"
        elif isinstance(self._value, complex):
            return "Complex"
        elif isinstance(self._value, str):
            return "String"
        elif isinstance(self._value, datetime):
            return "DateTime"
        return "Unknown"

    def __repr__(self) -> str:
        return f"Scalar({self._value!r})"

    def display(self) -> str:
        if isinstance(self._value, complex):
            real, imag = self._value.real, self._value.imag
            if real == 0:
                return f"{imag}i"
            elif imag >= 0:
                return f"{real} + {imag}i"
            else:
                return f"{real} - {-imag}i"
        elif isinstance(self._value, bool):
            return "true" if self._value else "false"
        elif isinstance(self._value, float):
            if self._value.is_integer():
                return str(int(self._value))
            return str(self._value)
        return str(self._value)

    def __add__(self, other: "Scalar") -> "Scalar":
        return Scalar(self._value + other._value)  # type: ignore

    def __sub__(self, other: "Scalar") -> "Scalar":
        return Scalar(self._value - other._value)  # type: ignore

    def __mul__(self, other: "Scalar") -> "Scalar":
        return Scalar(self._value * other._value)  # type: ignore

    def __truediv__(self, other: "Scalar") -> "Scalar":
        return Scalar(self._value / other._value)  # type: ignore

    def __pow__(self, other: "Scalar") -> "Scalar":
        return Scalar(self._value ** other._value)  # type: ignore

    def __neg__(self) -> "Scalar":
        return Scalar(-self._value)  # type: ignore

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Scalar):
            return self._value == other._value
        return False

    def __hash__(self) -> int:
        return hash(self._value)
