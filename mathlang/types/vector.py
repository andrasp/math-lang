"""Vector type for homogeneous arrays of scalars."""

from typing import Sequence

from mathlang.types.base import MathObject
from mathlang.types.scalar import Scalar, ScalarValue


class Vector(MathObject):
    """A homogeneous array of scalar values."""

    def __init__(self, values: Sequence[ScalarValue]):
        self._values = list(values)

    @property
    def values(self) -> list[ScalarValue]:
        return self._values

    def __len__(self) -> int:
        return len(self._values)

    def __getitem__(self, index: int) -> Scalar:
        return Scalar(self._values[index])

    @property
    def type_name(self) -> str:
        if not self._values:
            return "Vector (empty)"
        first = self._values[0]
        if isinstance(first, int):
            elem_type = "Integer"
        elif isinstance(first, float):
            elem_type = "Float"
        elif isinstance(first, complex):
            elem_type = "Complex"
        else:
            elem_type = type(first).__name__
        return f"Vector ({elem_type})"

    def __repr__(self) -> str:
        return f"Vector({self._values!r})"

    def display(self) -> str:
        if len(self._values) <= 10:
            items = ", ".join(Scalar(v).display() for v in self._values)
        else:
            first_items = ", ".join(Scalar(v).display() for v in self._values[:5])
            last_items = ", ".join(Scalar(v).display() for v in self._values[-3:])
            items = f"{first_items}, ..., {last_items}"
        return f"[{items}]"
