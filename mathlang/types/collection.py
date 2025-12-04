"""Collection types: List (heterogeneous) and Interval (range)."""

from typing import Iterator, Sequence
import math

from mathlang.types.base import MathObject


class List(MathObject):
    """A heterogeneous collection of MathObjects."""

    def __init__(self, items: Sequence[MathObject]):
        self._items = list(items)

    @property
    def items(self) -> list[MathObject]:
        return self._items

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int) -> MathObject:
        return self._items[index]

    def __iter__(self):
        return iter(self._items)

    @property
    def type_name(self) -> str:
        return f"List ({len(self._items)} items)"

    def __repr__(self) -> str:
        return f"List({self._items!r})"

    def display(self) -> str:
        if len(self._items) <= 10:
            items = ", ".join(item.display() for item in self._items)
        else:
            first_items = ", ".join(item.display() for item in self._items[:5])
            last_items = ", ".join(item.display() for item in self._items[-3:])
            items = f"{first_items}, ..., {last_items}"
        return f"[{items}]"


class Interval(MathObject):
    """A numeric range with start, end, and step. Lazy like a Python generator."""

    def __init__(self, start: float, end: float, step: float = 1.0):
        # Import here to avoid circular import
        from mathlang.types.scalar import Scalar
        self._Scalar = Scalar
        self._start = start
        self._end = end
        self._step = step

    @property
    def start(self) -> float:
        return self._start

    @property
    def end(self) -> float:
        return self._end

    @property
    def step(self) -> float:
        return self._step

    def __len__(self) -> int:
        """Return the number of elements in the interval."""
        if self._step > 0:
            if self._start >= self._end:
                return 0
            return max(0, math.ceil((self._end - self._start) / self._step))
        else:
            if self._start <= self._end:
                return 0
            return max(0, math.ceil((self._start - self._end) / abs(self._step)))

    def __iter__(self) -> Iterator[MathObject]:
        """Yield Scalar values lazily."""
        current = self._start
        if self._step > 0:
            while current < self._end:
                yield self._Scalar(current)
                current += self._step
        else:
            while current > self._end:
                yield self._Scalar(current)
                current += self._step

    def __getitem__(self, index: int) -> MathObject:
        """Get element at index."""
        if index < 0:
            index = len(self) + index
        if index < 0 or index >= len(self):
            raise IndexError(f"Interval index {index} out of range")
        return self._Scalar(self._start + index * self._step)

    def to_list(self) -> list[float]:
        """Generate all values in the interval as raw floats."""
        result = []
        current = self._start
        if self._step > 0:
            while current < self._end:
                result.append(current)
                current += self._step
        else:
            while current > self._end:
                result.append(current)
                current += self._step
        return result

    @property
    def type_name(self) -> str:
        return "Interval"

    def __repr__(self) -> str:
        return f"Interval({self._start}, {self._end}, step={self._step})"

    def display(self) -> str:
        if self._step == 1.0:
            return f"[{self._start}..{self._end})"
        return f"[{self._start}..{self._end} step {self._step})"
