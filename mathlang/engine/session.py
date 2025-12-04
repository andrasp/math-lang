"""Evaluation session with variable scope."""

from typing import Any

from mathlang.types.base import MathObject


class Session:
    """
    An evaluation session that maintains variable state.

    Each session has its own variable scope. Sessions can be nested
    for custom operation execution with local variables.
    """

    def __init__(self, parent: "Session | None" = None):
        self._variables: dict[str, MathObject] = {}
        self._parent = parent

    def get(self, name: str) -> MathObject | None:
        """Get a variable value, checking parent scopes if not found locally."""
        if name in self._variables:
            return self._variables[name]
        if self._parent is not None:
            return self._parent.get(name)
        return None

    def set(self, name: str, value: MathObject) -> None:
        """Set a variable in the current scope."""
        self._variables[name] = value

    def has(self, name: str) -> bool:
        """Check if a variable exists in any scope."""
        return self.get(name) is not None

    def delete(self, name: str) -> bool:
        """Delete a variable from the current scope. Returns True if deleted."""
        if name in self._variables:
            del self._variables[name]
            return True
        return False

    def clear(self) -> None:
        """Clear all variables in the current scope."""
        self._variables.clear()

    def list_variables(self) -> dict[str, MathObject]:
        """Get all variables visible in this scope (including parent scopes)."""
        result = {}
        if self._parent is not None:
            result.update(self._parent.list_variables())
        result.update(self._variables)
        return result

    def create_child(self) -> "Session":
        """Create a child session that inherits from this one."""
        return Session(parent=self)
