"""Operation system for MathLang."""

from mathlang.operations.base import Operation, OperationProvider
from mathlang.operations.registry import register_provider, get_operation, list_operations

__all__ = [
    "Operation",
    "OperationProvider",
    "register_provider",
    "get_operation",
    "list_operations",
]
