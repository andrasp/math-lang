"""Logical operations: And, Or, Not, etc."""

from typing import TYPE_CHECKING

from mathlang.operations.base import Operation, OperationProvider, ArgInfo
from mathlang.types.scalar import Scalar
from mathlang.types.coercion import is_truthy
from mathlang.types.callable import Thunk
from mathlang.engine.errors import TypeError

if TYPE_CHECKING:
    from mathlang.types.base import MathObject
    from mathlang.engine.session import Session


class LogicalProvider(OperationProvider):
    """Provider for logical operations."""

    @property
    def name(self) -> str:
        return "Logical"

    def _register_operations(self) -> None:
        self.register(Operation(
            identifier="And",
            friendly_name="Logical And",
            description="Returns true if all arguments are truthy",
            category="Logical/Boolean",
            has_variable_args=True,
            variable_arg_info=ArgInfo("values", "Values to check"),
            execute=self._and,
        ))

        self.register(Operation(
            identifier="Or",
            friendly_name="Logical Or",
            description="Returns true if any argument is truthy",
            category="Logical/Boolean",
            has_variable_args=True,
            variable_arg_info=ArgInfo("values", "Values to check"),
            execute=self._or,
        ))

        self.register(Operation(
            identifier="Not",
            friendly_name="Logical Not",
            description="Returns the logical negation of a value",
            category="Logical/Boolean",
            required_args=[ArgInfo("x", "Value to negate")],
            execute=self._not,
        ))

        self.register(Operation(
            identifier="If",
            friendly_name="Conditional",
            description="Returns then_value if condition is truthy, else else_value",
            category="Logical/Control",
            required_args=[
                ArgInfo("condition", "Condition to check"),
                ArgInfo("then_value", "Value if true"),
                ArgInfo("else_value", "Value if false"),
            ],
            execute=self._if,
            # Lazy evaluation for then/else branches (indices 1 and 2)
            # Enables recursion by only evaluating the taken branch
            lazy_arg_indices={1, 2},
        ))

        self.register(Operation(
            identifier="IsNaN",
            friendly_name="Is Not a Number",
            description="Returns true if the value is NaN",
            category="Logical/Checks",
            required_args=[ArgInfo("x", "Value to check")],
            execute=self._is_nan,
        ))

        self.register(Operation(
            identifier="IsInf",
            friendly_name="Is Infinite",
            description="Returns true if the value is positive or negative infinity",
            category="Logical/Checks",
            required_args=[ArgInfo("x", "Value to check")],
            execute=self._is_inf,
        ))

    def _and(self, args: list["MathObject"], session: "Session") -> "MathObject":
        for arg in args:
            if not is_truthy(arg):
                return Scalar(False)
        return Scalar(True)

    def _or(self, args: list["MathObject"], session: "Session") -> "MathObject":
        for arg in args:
            if is_truthy(arg):
                return Scalar(True)
        return Scalar(False)

    def _not(self, args: list["MathObject"], session: "Session") -> "MathObject":
        return Scalar(not is_truthy(args[0]))

    def _if(self, args: list["MathObject"], session: "Session") -> "MathObject":
        condition, then_value, else_value = args
        if is_truthy(condition):
            # Force evaluation of the then branch
            return then_value.force() if isinstance(then_value, Thunk) else then_value
        # Force evaluation of the else branch
        return else_value.force() if isinstance(else_value, Thunk) else else_value

    def _is_nan(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x = args[0]
        if not isinstance(x, Scalar):
            return Scalar(False)
        import math
        val = x.value
        if isinstance(val, (int, float)):
            return Scalar(math.isnan(val))
        return Scalar(False)

    def _is_inf(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x = args[0]
        if not isinstance(x, Scalar):
            return Scalar(False)
        import math
        val = x.value
        if isinstance(val, (int, float)):
            return Scalar(math.isinf(val))
        return Scalar(False)
