"""Callable types: Lambda (anonymous functions) and Thunk (deferred expressions)."""

from typing import TYPE_CHECKING

from mathlang.types.base import MathObject
from mathlang.lang.ast import expr_to_string

if TYPE_CHECKING:
    from mathlang.lang.ast import Expression
    from mathlang.engine.session import Session


class Thunk(MathObject):
    """A deferred expression that hasn't been evaluated yet.

    Used for lazy evaluation in operations like If that need to
    conditionally evaluate their arguments.
    """

    def __init__(self, expression: "Expression", session: "Session"):
        self._expression = expression
        self._session = session

    @property
    def expression(self) -> "Expression":
        return self._expression

    @property
    def session(self) -> "Session":
        return self._session

    def force(self) -> "MathObject":
        """Evaluate the thunk and return the result."""
        from mathlang.engine.evaluator import evaluate_expression
        return evaluate_expression(self._expression, self._session)

    @property
    def type_name(self) -> str:
        return "Thunk"

    def __repr__(self) -> str:
        return "Thunk(...)"

    def display(self) -> str:
        return "<deferred>"


class Lambda(MathObject):
    """An anonymous function (lambda expression)."""

    def __init__(self, parameters: list[str], body: "Expression"):
        self._parameters = parameters
        self._body = body

    @property
    def parameters(self) -> list[str]:
        return self._parameters

    @property
    def body(self) -> "Expression":
        return self._body

    @property
    def arity(self) -> int:
        """Number of parameters."""
        return len(self._parameters)

    @property
    def type_name(self) -> str:
        return f"Lambda ({self.arity} params)"

    def __repr__(self) -> str:
        params = ", ".join(self._parameters) if self._parameters else "()"
        return f"Lambda({params} -> ...)"

    def display(self) -> str:
        body_str = expr_to_string(self._body)
        if not self._parameters:
            return f"() -> {body_str}"
        elif len(self._parameters) == 1:
            return f"{self._parameters[0]} -> {body_str}"
        else:
            return f"({', '.join(self._parameters)}) -> {body_str}"
