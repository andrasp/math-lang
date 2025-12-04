"""Runtime error definitions."""

from mathlang.lang.errors import MathLangError


class RuntimeError(MathLangError):
    """Base class for runtime errors."""
    pass


class UndefinedVariableError(RuntimeError):
    """Raised when referencing an undefined variable."""

    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Undefined variable: '{name}'")


class UndefinedOperationError(RuntimeError):
    """Raised when calling an undefined operation/function."""

    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Undefined operation: '{name}'")


class TypeError(RuntimeError):
    """Raised for type mismatches in operations."""

    def __init__(self, message: str):
        super().__init__(message)


class ArgumentError(RuntimeError):
    """Raised for incorrect arguments to operations."""

    def __init__(self, message: str):
        super().__init__(message)


class DivisionByZeroError(RuntimeError):
    """Raised when dividing by zero."""

    def __init__(self):
        super().__init__("Division by zero")
