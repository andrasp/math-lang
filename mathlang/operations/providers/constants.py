"""Named constants: PI, E, PHI, etc."""

import math
from typing import TYPE_CHECKING

from mathlang.operations.base import Operation, OperationProvider
from mathlang.types.scalar import Scalar

if TYPE_CHECKING:
    from mathlang.types.base import MathObject
    from mathlang.engine.session import Session


# Golden ratio
PHI = (1 + math.sqrt(5)) / 2


class ConstantsProvider(OperationProvider):
    """Provider for named constants."""

    @property
    def name(self) -> str:
        return "Constants"

    def _register_operations(self) -> None:
        # Mathematical constants
        self.register(Operation(
            identifier="PI",
            friendly_name="Pi",
            description="The mathematical constant π (3.14159...)",
            category="Constants/Mathematical",
            execute=lambda args, session: Scalar(math.pi),
        ))

        self.register(Operation(
            identifier="E",
            friendly_name="Euler's Number",
            description="The mathematical constant e (2.71828...)",
            category="Constants/Mathematical",
            execute=lambda args, session: Scalar(math.e),
        ))

        self.register(Operation(
            identifier="PHI",
            friendly_name="Golden Ratio",
            description="The golden ratio φ (1.61803...)",
            category="Constants/Mathematical",
            execute=lambda args, session: Scalar(PHI),
        ))

        self.register(Operation(
            identifier="TAU",
            friendly_name="Tau",
            description="The mathematical constant τ = 2π (6.28318...)",
            category="Constants/Mathematical",
            execute=lambda args, session: Scalar(math.tau),
        ))

        self.register(Operation(
            identifier="INF",
            friendly_name="Infinity",
            description="Positive infinity",
            category="Constants/Special",
            execute=lambda args, session: Scalar(math.inf),
        ))

        self.register(Operation(
            identifier="NAN",
            friendly_name="Not a Number",
            description="Not a Number (NaN)",
            category="Constants/Special",
            execute=lambda args, session: Scalar(math.nan),
        ))

        # Unit conversions
        self.register(Operation(
            identifier="HoursInDay",
            friendly_name="Hours in a Day",
            description="Number of hours in a day (24)",
            category="Constants/Time",
            execute=lambda args, session: Scalar(24),
        ))

        self.register(Operation(
            identifier="MinutesInHour",
            friendly_name="Minutes in an Hour",
            description="Number of minutes in an hour (60)",
            category="Constants/Time",
            execute=lambda args, session: Scalar(60),
        ))

        self.register(Operation(
            identifier="SecondsInMinute",
            friendly_name="Seconds in a Minute",
            description="Number of seconds in a minute (60)",
            category="Constants/Time",
            execute=lambda args, session: Scalar(60),
        ))

        # Physics constants (common ones)
        self.register(Operation(
            identifier="SpeedOfLight",
            friendly_name="Speed of Light",
            description="Speed of light in m/s (299792458)",
            category="Constants/Physics",
            execute=lambda args, session: Scalar(299792458),
        ))

        self.register(Operation(
            identifier="GravitationalConstant",
            friendly_name="Gravitational Constant",
            description="Gravitational constant G in m³/(kg·s²)",
            category="Constants/Physics",
            execute=lambda args, session: Scalar(6.67430e-11),
        ))

        self.register(Operation(
            identifier="PlanckConstant",
            friendly_name="Planck Constant",
            description="Planck constant h in J·s",
            category="Constants/Physics",
            execute=lambda args, session: Scalar(6.62607015e-34),
        ))
