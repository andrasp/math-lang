"""Arithmetic operations: Abs, Round, Floor, Ceiling, Sqrt, Random, etc."""

import math
import random
from typing import TYPE_CHECKING

from mathlang.operations.base import Operation, OperationProvider, ArgInfo
from mathlang.types.scalar import Scalar
from mathlang.engine.errors import TypeError, ArgumentError

if TYPE_CHECKING:
    from mathlang.types.base import MathObject
    from mathlang.engine.session import Session


class ArithmeticProvider(OperationProvider):
    """Provider for arithmetic operations."""

    @property
    def name(self) -> str:
        return "Arithmetic"

    def _register_operations(self) -> None:
        self.register(Operation(
            identifier="Abs",
            friendly_name="Absolute Value",
            description="Returns the absolute value of a number",
            category="Arithmetic/Basic",
            required_args=[ArgInfo("x", "The number")],
            execute=self._abs,
        ))

        self.register(Operation(
            identifier="Sqrt",
            friendly_name="Square Root",
            description="Returns the square root of a number",
            category="Arithmetic/Basic",
            required_args=[ArgInfo("x", "The number (must be non-negative)")],
            execute=self._sqrt,
        ))

        self.register(Operation(
            identifier="Floor",
            friendly_name="Floor",
            description="Returns the largest integer less than or equal to x",
            category="Arithmetic/Rounding",
            required_args=[ArgInfo("x", "The number")],
            execute=self._floor,
        ))

        self.register(Operation(
            identifier="Ceiling",
            friendly_name="Ceiling",
            description="Returns the smallest integer greater than or equal to x",
            category="Arithmetic/Rounding",
            required_args=[ArgInfo("x", "The number")],
            execute=self._ceiling,
        ))

        self.register(Operation(
            identifier="Round",
            friendly_name="Round",
            description="Rounds a number to the nearest integer or specified decimal places",
            category="Arithmetic/Rounding",
            required_args=[ArgInfo("x", "The number")],
            optional_args=[ArgInfo("decimals", "Number of decimal places", default=0)],
            execute=self._round,
        ))

        self.register(Operation(
            identifier="Log",
            friendly_name="Natural Logarithm",
            description="Returns the natural logarithm of a number",
            category="Arithmetic/Logarithms",
            required_args=[ArgInfo("x", "The number (must be positive)")],
            execute=self._log,
        ))

        self.register(Operation(
            identifier="Log10",
            friendly_name="Base-10 Logarithm",
            description="Returns the base-10 logarithm of a number",
            category="Arithmetic/Logarithms",
            required_args=[ArgInfo("x", "The number (must be positive)")],
            execute=self._log10,
        ))

        self.register(Operation(
            identifier="Exp",
            friendly_name="Exponential",
            description="Returns e raised to the power of x",
            category="Arithmetic/Exponential",
            required_args=[ArgInfo("x", "The exponent")],
            execute=self._exp,
        ))

        self.register(Operation(
            identifier="Min",
            friendly_name="Minimum",
            description="Returns the smallest of the given numbers",
            category="Arithmetic/Comparison",
            has_variable_args=True,
            variable_arg_info=ArgInfo("numbers", "Numbers to compare"),
            execute=self._min,
        ))

        self.register(Operation(
            identifier="Max",
            friendly_name="Maximum",
            description="Returns the largest of the given numbers",
            category="Arithmetic/Comparison",
            has_variable_args=True,
            variable_arg_info=ArgInfo("numbers", "Numbers to compare"),
            execute=self._max,
        ))

        self.register(Operation(
            identifier="Random",
            friendly_name="Random",
            description="Returns a random number. With no args: [0, 1). With one arg n: integer [0, n). With two args a, b: [a, b).",
            category="Arithmetic/Random",
            optional_args=[
                ArgInfo("a", "Upper bound (exclusive) or lower bound if b provided"),
                ArgInfo("b", "Upper bound (exclusive)"),
            ],
            execute=self._random,
        ))

    def _abs(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x = args[0]
        if not isinstance(x, Scalar):
            raise TypeError(f"Abs expects a number, got {x.type_name}")
        return Scalar(abs(x.value))

    def _sqrt(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x = args[0]
        if not isinstance(x, Scalar):
            raise TypeError(f"Sqrt expects a number, got {x.type_name}")
        val = x.value
        if isinstance(val, complex):
            return Scalar(val ** 0.5)
        if val < 0:
            return Scalar(complex(val) ** 0.5)
        return Scalar(math.sqrt(val))

    def _floor(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x = args[0]
        if not isinstance(x, Scalar):
            raise TypeError(f"Floor expects a number, got {x.type_name}")
        return Scalar(math.floor(x.value))

    def _ceiling(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x = args[0]
        if not isinstance(x, Scalar):
            raise TypeError(f"Ceiling expects a number, got {x.type_name}")
        return Scalar(math.ceil(x.value))

    def _round(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x = args[0]
        if not isinstance(x, Scalar):
            raise TypeError(f"Round expects a number, got {x.type_name}")
        decimals = 0
        if len(args) > 1:
            if not isinstance(args[1], Scalar):
                raise TypeError(f"Round decimals must be an integer, got {args[1].type_name}")
            decimals = int(args[1].value)
        return Scalar(round(x.value, decimals))

    def _log(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x = args[0]
        if not isinstance(x, Scalar):
            raise TypeError(f"Log expects a number, got {x.type_name}")
        val = x.value
        if isinstance(val, complex):
            import cmath
            return Scalar(cmath.log(val))
        if val <= 0:
            raise ArgumentError("Log requires a positive number")
        return Scalar(math.log(val))

    def _log10(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x = args[0]
        if not isinstance(x, Scalar):
            raise TypeError(f"Log10 expects a number, got {x.type_name}")
        val = x.value
        if isinstance(val, complex):
            import cmath
            return Scalar(cmath.log10(val))
        if val <= 0:
            raise ArgumentError("Log10 requires a positive number")
        return Scalar(math.log10(val))

    def _exp(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x = args[0]
        if not isinstance(x, Scalar):
            raise TypeError(f"Exp expects a number, got {x.type_name}")
        val = x.value
        if isinstance(val, complex):
            import cmath
            return Scalar(cmath.exp(val))
        return Scalar(math.exp(val))

    def _min(self, args: list["MathObject"], session: "Session") -> "MathObject":
        if not args:
            raise ArgumentError("Min requires at least one argument")
        values = []
        for arg in args:
            if not isinstance(arg, Scalar):
                raise TypeError(f"Min expects numbers, got {arg.type_name}")
            values.append(arg.value)
        return Scalar(min(values))

    def _max(self, args: list["MathObject"], session: "Session") -> "MathObject":
        if not args:
            raise ArgumentError("Max requires at least one argument")
        values = []
        for arg in args:
            if not isinstance(arg, Scalar):
                raise TypeError(f"Max expects numbers, got {arg.type_name}")
            values.append(arg.value)
        return Scalar(max(values))

    def _random(self, args: list["MathObject"], session: "Session") -> "MathObject":
        if len(args) == 0:
            return Scalar(random.random())
        elif len(args) == 1:
            if not isinstance(args[0], Scalar):
                raise TypeError(f"Random expects a number, got {args[0].type_name}")
            n = int(args[0].value)
            return Scalar(random.randint(0, n - 1))
        else:
            if not isinstance(args[0], Scalar) or not isinstance(args[1], Scalar):
                raise TypeError("Random expects numbers")
            a = args[0].value
            b = args[1].value
            return Scalar(random.uniform(a, b))
