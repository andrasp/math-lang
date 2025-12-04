"""Trigonometry operations: Sin, Cos, Tan, etc."""

import math
import cmath
from typing import TYPE_CHECKING

from mathlang.operations.base import Operation, OperationProvider, ArgInfo
from mathlang.types.scalar import Scalar
from mathlang.engine.errors import TypeError

if TYPE_CHECKING:
    from mathlang.types.base import MathObject
    from mathlang.engine.session import Session


class TrigonometryProvider(OperationProvider):
    """Provider for trigonometric operations."""

    @property
    def name(self) -> str:
        return "Trigonometry"

    def _register_operations(self) -> None:
        # Basic trig functions
        self.register(Operation(
            identifier="Sin",
            friendly_name="Sine",
            description="Returns the sine of an angle (in radians)",
            category="Trigonometry/Basic",
            required_args=[ArgInfo("x", "Angle in radians")],
            execute=self._sin,
        ))

        self.register(Operation(
            identifier="Cos",
            friendly_name="Cosine",
            description="Returns the cosine of an angle (in radians)",
            category="Trigonometry/Basic",
            required_args=[ArgInfo("x", "Angle in radians")],
            execute=self._cos,
        ))

        self.register(Operation(
            identifier="Tan",
            friendly_name="Tangent",
            description="Returns the tangent of an angle (in radians)",
            category="Trigonometry/Basic",
            required_args=[ArgInfo("x", "Angle in radians")],
            execute=self._tan,
        ))

        # Inverse trig functions
        self.register(Operation(
            identifier="ArcSin",
            friendly_name="Arcsine",
            description="Returns the arcsine (inverse sine) in radians",
            category="Trigonometry/Inverse",
            required_args=[ArgInfo("x", "Value between -1 and 1")],
            execute=self._asin,
        ))

        self.register(Operation(
            identifier="ArcCos",
            friendly_name="Arccosine",
            description="Returns the arccosine (inverse cosine) in radians",
            category="Trigonometry/Inverse",
            required_args=[ArgInfo("x", "Value between -1 and 1")],
            execute=self._acos,
        ))

        self.register(Operation(
            identifier="ArcTan",
            friendly_name="Arctangent",
            description="Returns the arctangent (inverse tangent) in radians",
            category="Trigonometry/Inverse",
            required_args=[ArgInfo("x", "Any real number")],
            execute=self._atan,
        ))

        self.register(Operation(
            identifier="ArcTan2",
            friendly_name="Arctangent2",
            description="Returns the arctangent of y/x, using signs to determine quadrant",
            category="Trigonometry/Inverse",
            required_args=[
                ArgInfo("y", "Y coordinate"),
                ArgInfo("x", "X coordinate"),
            ],
            execute=self._atan2,
        ))

        # Hyperbolic functions
        self.register(Operation(
            identifier="Sinh",
            friendly_name="Hyperbolic Sine",
            description="Returns the hyperbolic sine",
            category="Trigonometry/Hyperbolic",
            required_args=[ArgInfo("x", "Any number")],
            execute=self._sinh,
        ))

        self.register(Operation(
            identifier="Cosh",
            friendly_name="Hyperbolic Cosine",
            description="Returns the hyperbolic cosine",
            category="Trigonometry/Hyperbolic",
            required_args=[ArgInfo("x", "Any number")],
            execute=self._cosh,
        ))

        self.register(Operation(
            identifier="Tanh",
            friendly_name="Hyperbolic Tangent",
            description="Returns the hyperbolic tangent",
            category="Trigonometry/Hyperbolic",
            required_args=[ArgInfo("x", "Any number")],
            execute=self._tanh,
        ))

        # Conversion
        self.register(Operation(
            identifier="ToRadians",
            friendly_name="Degrees to Radians",
            description="Converts degrees to radians",
            category="Trigonometry/Conversion",
            required_args=[ArgInfo("degrees", "Angle in degrees")],
            execute=self._to_radians,
        ))

        self.register(Operation(
            identifier="ToDegrees",
            friendly_name="Radians to Degrees",
            description="Converts radians to degrees",
            category="Trigonometry/Conversion",
            required_args=[ArgInfo("radians", "Angle in radians")],
            execute=self._to_degrees,
        ))

    def _get_value(self, arg: "MathObject") -> complex | float:
        if not isinstance(arg, Scalar):
            raise TypeError(f"Expected a number, got {arg.type_name}")
        return arg.value

    def _sin(self, args: list["MathObject"], session: "Session") -> "MathObject":
        val = self._get_value(args[0])
        if isinstance(val, complex):
            return Scalar(cmath.sin(val))
        return Scalar(math.sin(val))

    def _cos(self, args: list["MathObject"], session: "Session") -> "MathObject":
        val = self._get_value(args[0])
        if isinstance(val, complex):
            return Scalar(cmath.cos(val))
        return Scalar(math.cos(val))

    def _tan(self, args: list["MathObject"], session: "Session") -> "MathObject":
        val = self._get_value(args[0])
        if isinstance(val, complex):
            return Scalar(cmath.tan(val))
        return Scalar(math.tan(val))

    def _asin(self, args: list["MathObject"], session: "Session") -> "MathObject":
        val = self._get_value(args[0])
        if isinstance(val, complex):
            return Scalar(cmath.asin(val))
        if val < -1 or val > 1:
            return Scalar(cmath.asin(complex(val)))
        return Scalar(math.asin(val))

    def _acos(self, args: list["MathObject"], session: "Session") -> "MathObject":
        val = self._get_value(args[0])
        if isinstance(val, complex):
            return Scalar(cmath.acos(val))
        if val < -1 or val > 1:
            return Scalar(cmath.acos(complex(val)))
        return Scalar(math.acos(val))

    def _atan(self, args: list["MathObject"], session: "Session") -> "MathObject":
        val = self._get_value(args[0])
        if isinstance(val, complex):
            return Scalar(cmath.atan(val))
        return Scalar(math.atan(val))

    def _atan2(self, args: list["MathObject"], session: "Session") -> "MathObject":
        y = self._get_value(args[0])
        x = self._get_value(args[1])
        if isinstance(y, complex) or isinstance(x, complex):
            raise TypeError("ArcTan2 does not support complex numbers")
        return Scalar(math.atan2(y, x))

    def _sinh(self, args: list["MathObject"], session: "Session") -> "MathObject":
        val = self._get_value(args[0])
        if isinstance(val, complex):
            return Scalar(cmath.sinh(val))
        return Scalar(math.sinh(val))

    def _cosh(self, args: list["MathObject"], session: "Session") -> "MathObject":
        val = self._get_value(args[0])
        if isinstance(val, complex):
            return Scalar(cmath.cosh(val))
        return Scalar(math.cosh(val))

    def _tanh(self, args: list["MathObject"], session: "Session") -> "MathObject":
        val = self._get_value(args[0])
        if isinstance(val, complex):
            return Scalar(cmath.tanh(val))
        return Scalar(math.tanh(val))

    def _to_radians(self, args: list["MathObject"], session: "Session") -> "MathObject":
        val = self._get_value(args[0])
        return Scalar(math.radians(val))

    def _to_degrees(self, args: list["MathObject"], session: "Session") -> "MathObject":
        val = self._get_value(args[0])
        return Scalar(math.degrees(val))
