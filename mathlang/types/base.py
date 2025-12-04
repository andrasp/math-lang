"""Base class for all MathLang values."""

from abc import ABC, abstractmethod
from typing import Any


class MathObject(ABC):
    """Base class for all values in the MathLang type system."""

    @abstractmethod
    def __repr__(self) -> str:
        """Return a string representation for debugging."""
        pass

    @abstractmethod
    def display(self) -> str:
        """Return a user-friendly string representation."""
        pass

    @property
    @abstractmethod
    def type_name(self) -> str:
        """Return the type name for display purposes."""
        pass
