"""Base classes for operations and providers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, Any

if TYPE_CHECKING:
    from mathlang.types.base import MathObject
    from mathlang.engine.session import Session


@dataclass
class ArgInfo:
    """Information about an operation argument."""

    name: str
    description: str = ""
    accepted_types: list[str] = field(default_factory=lambda: ["Any"])
    optional: bool = False
    default: Any = None


@dataclass
class Operation:
    """Definition of an executable operation."""

    identifier: str
    friendly_name: str
    description: str
    category: str  # For UI tree organization (e.g., "Arithmetic/Basic")
    execute: Callable[[list["MathObject"], "Session"], "MathObject"]
    required_args: list[ArgInfo] = field(default_factory=list)
    optional_args: list[ArgInfo] = field(default_factory=list)
    has_variable_args: bool = False
    variable_arg_info: ArgInfo | None = None
    # Indices of arguments that should be passed as unevaluated expressions (for lazy eval)
    # Used by operations like If that need to evaluate branches conditionally
    lazy_arg_indices: set[int] = field(default_factory=set)

    @property
    def min_args(self) -> int:
        return len(self.required_args)

    @property
    def max_args(self) -> int | None:
        if self.has_variable_args:
            return None
        return len(self.required_args) + len(self.optional_args)


class OperationProvider(ABC):
    """
    Base class for operation providers.

    Each provider groups related operations (e.g., ArithmeticProvider, TrigProvider).
    Providers register their operations in __init__.
    """

    def __init__(self):
        self._operations: dict[str, Operation] = {}
        self._register_operations()

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name for identification."""
        pass

    @abstractmethod
    def _register_operations(self) -> None:
        """Register all operations this provider offers."""
        pass

    def register(self, operation: Operation) -> None:
        """Register an operation with this provider."""
        self._operations[operation.identifier] = operation

    def get(self, identifier: str) -> Operation | None:
        """Get an operation by identifier."""
        return self._operations.get(identifier)

    def list_operations(self) -> list[Operation]:
        """List all operations from this provider."""
        return list(self._operations.values())
