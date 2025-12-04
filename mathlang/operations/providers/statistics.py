"""Statistics operations: Mean, Median, StdDev, Variance, etc."""

import math
from typing import TYPE_CHECKING

from mathlang.operations.base import Operation, OperationProvider, ArgInfo
from mathlang.types.scalar import Scalar
from mathlang.types.collection import List, Interval
from mathlang.engine.errors import TypeError, ArgumentError


def _is_collection(obj: "MathObject") -> bool:
    """Check if an object is a collection (List or Interval)."""
    return isinstance(obj, (List, Interval))

if TYPE_CHECKING:
    from mathlang.types.base import MathObject
    from mathlang.engine.session import Session


class StatisticsProvider(OperationProvider):
    """Provider for statistics operations."""

    @property
    def name(self) -> str:
        return "Statistics"

    def _register_operations(self) -> None:
        self.register(Operation(
            identifier="Mean",
            friendly_name="Mean (Average)",
            description="Calculates the arithmetic mean of a list of numbers",
            category="Statistics/Central",
            required_args=[ArgInfo("list", "List of numbers")],
            execute=self._mean,
        ))

        self.register(Operation(
            identifier="Median",
            friendly_name="Median",
            description="Calculates the median value of a list of numbers",
            category="Statistics/Central",
            required_args=[ArgInfo("list", "List of numbers")],
            execute=self._median,
        ))

        self.register(Operation(
            identifier="Mode",
            friendly_name="Mode",
            description="Finds the most common value(s) in a list",
            category="Statistics/Central",
            required_args=[ArgInfo("list", "List of values")],
            execute=self._mode,
        ))

        self.register(Operation(
            identifier="StdDev",
            friendly_name="Standard Deviation",
            description="Calculates the sample standard deviation",
            category="Statistics/Spread",
            required_args=[ArgInfo("list", "List of numbers")],
            execute=self._stddev,
        ))

        self.register(Operation(
            identifier="PopStdDev",
            friendly_name="Population Standard Deviation",
            description="Calculates the population standard deviation",
            category="Statistics/Spread",
            required_args=[ArgInfo("list", "List of numbers")],
            execute=self._pop_stddev,
        ))

        self.register(Operation(
            identifier="Variance",
            friendly_name="Variance",
            description="Calculates the sample variance",
            category="Statistics/Spread",
            required_args=[ArgInfo("list", "List of numbers")],
            execute=self._variance,
        ))

        self.register(Operation(
            identifier="PopVariance",
            friendly_name="Population Variance",
            description="Calculates the population variance",
            category="Statistics/Spread",
            required_args=[ArgInfo("list", "List of numbers")],
            execute=self._pop_variance,
        ))

        self.register(Operation(
            identifier="Correlation",
            friendly_name="Correlation",
            description="Calculates the Pearson correlation coefficient between two lists",
            category="Statistics/Relationship",
            required_args=[
                ArgInfo("list1", "First list of numbers"),
                ArgInfo("list2", "Second list of numbers"),
            ],
            execute=self._correlation,
        ))

        self.register(Operation(
            identifier="Covariance",
            friendly_name="Covariance",
            description="Calculates the sample covariance between two lists",
            category="Statistics/Relationship",
            required_args=[
                ArgInfo("list1", "First list of numbers"),
                ArgInfo("list2", "Second list of numbers"),
            ],
            execute=self._covariance,
        ))

        self.register(Operation(
            identifier="LinearRegression",
            friendly_name="Linear Regression",
            description="Performs linear regression, returns [slope, intercept, r_squared]",
            category="Statistics/Regression",
            required_args=[
                ArgInfo("x_values", "X values (independent variable)"),
                ArgInfo("y_values", "Y values (dependent variable)"),
            ],
            execute=self._linear_regression,
        ))

        self.register(Operation(
            identifier="Percentile",
            friendly_name="Percentile",
            description="Calculates the nth percentile of a list",
            category="Statistics/Quantile",
            required_args=[
                ArgInfo("list", "List of numbers"),
                ArgInfo("n", "Percentile (0-100)"),
            ],
            execute=self._percentile,
        ))

        self.register(Operation(
            identifier="Quartiles",
            friendly_name="Quartiles",
            description="Returns the quartiles [Q1, Q2, Q3] of a list",
            category="Statistics/Quantile",
            required_args=[ArgInfo("list", "List of numbers")],
            execute=self._quartiles,
        ))

        self.register(Operation(
            identifier="IQR",
            friendly_name="Interquartile Range",
            description="Calculates the interquartile range (Q3 - Q1)",
            category="Statistics/Spread",
            required_args=[ArgInfo("list", "List of numbers")],
            execute=self._iqr,
        ))

    def _extract_numbers(self, coll: "MathObject", name: str = "collection") -> list[float]:
        """Extract a list of numeric values from a MathObject (List or Interval)."""
        if not _is_collection(coll):
            raise TypeError(f"{name} must be a collection, got {coll.type_name}")

        # For Interval, use the optimized to_list() method
        if isinstance(coll, Interval):
            return coll.to_list()

        values = []
        for item in coll:
            if not isinstance(item, Scalar) or isinstance(item.value, str):
                raise TypeError(f"{name} must contain only numbers, got {item.type_name}")
            values.append(float(item.value))
        return values

    def _mean(self, args: list["MathObject"], session: "Session") -> "MathObject":
        values = self._extract_numbers(args[0])
        if not values:
            raise ArgumentError("Cannot calculate mean of empty list")
        return Scalar(sum(values) / len(values))

    def _median(self, args: list["MathObject"], session: "Session") -> "MathObject":
        values = self._extract_numbers(args[0])
        if not values:
            raise ArgumentError("Cannot calculate median of empty list")

        sorted_values = sorted(values)
        n = len(sorted_values)
        mid = n // 2

        if n % 2 == 0:
            return Scalar((sorted_values[mid - 1] + sorted_values[mid]) / 2)
        return Scalar(sorted_values[mid])

    def _mode(self, args: list["MathObject"], session: "Session") -> "MathObject":
        coll = args[0]
        if not _is_collection(coll):
            raise TypeError(f"collection must be a collection, got {coll.type_name}")
        if len(coll) == 0:
            raise ArgumentError("Cannot calculate mode of empty collection")

        counts: dict[str, tuple["MathObject", int]] = {}
        for item in coll:  # Works with any iterable (List or Interval)
            key = item.display()
            if key in counts:
                counts[key] = (counts[key][0], counts[key][1] + 1)
            else:
                counts[key] = (item, 1)

        max_count = max(c[1] for c in counts.values())
        modes = [v[0] for v in counts.values() if v[1] == max_count]

        if len(modes) == 1:
            return modes[0]
        return List(modes)

    def _calculate_variance(self, values: list[float], sample: bool = True) -> float:
        """Calculate variance using Welford's online algorithm (single-pass, numerically stable)."""
        n = len(values)
        if n < 2:
            raise ArgumentError("Need at least 2 values to calculate variance")

        # Welford's algorithm: single pass, numerically stable
        mean = 0.0
        m2 = 0.0
        for i, x in enumerate(values, 1):
            delta = x - mean
            mean += delta / i
            delta2 = x - mean
            m2 += delta * delta2

        divisor = n - 1 if sample else n
        return m2 / divisor

    def _variance(self, args: list["MathObject"], session: "Session") -> "MathObject":
        values = self._extract_numbers(args[0])
        return Scalar(self._calculate_variance(values, sample=True))

    def _pop_variance(self, args: list["MathObject"], session: "Session") -> "MathObject":
        values = self._extract_numbers(args[0])
        return Scalar(self._calculate_variance(values, sample=False))

    def _stddev(self, args: list["MathObject"], session: "Session") -> "MathObject":
        values = self._extract_numbers(args[0])
        return Scalar(math.sqrt(self._calculate_variance(values, sample=True)))

    def _pop_stddev(self, args: list["MathObject"], session: "Session") -> "MathObject":
        values = self._extract_numbers(args[0])
        return Scalar(math.sqrt(self._calculate_variance(values, sample=False)))

    def _correlation(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x_values = self._extract_numbers(args[0], "list1")
        y_values = self._extract_numbers(args[1], "list2")

        if len(x_values) != len(y_values):
            raise ArgumentError(f"Lists must have same length: {len(x_values)} vs {len(y_values)}")
        if len(x_values) < 2:
            raise ArgumentError("Need at least 2 values to calculate correlation")

        # Single-pass algorithm using online covariance
        n = 0
        mean_x = 0.0
        mean_y = 0.0
        c = 0.0  # Co-moment
        m2_x = 0.0  # Sum of squared deviations for x
        m2_y = 0.0  # Sum of squared deviations for y

        for x, y in zip(x_values, y_values):
            n += 1
            dx = x - mean_x
            mean_x += dx / n
            dy = y - mean_y
            mean_y += dy / n
            # Update co-moment and variances
            c += dx * (y - mean_y)
            m2_x += dx * (x - mean_x)
            m2_y += dy * (y - mean_y)

        if m2_x == 0 or m2_y == 0:
            return Scalar(0.0)

        return Scalar(c / math.sqrt(m2_x * m2_y))

    def _covariance(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x_values = self._extract_numbers(args[0], "list1")
        y_values = self._extract_numbers(args[1], "list2")

        if len(x_values) != len(y_values):
            raise ArgumentError(f"Lists must have same length: {len(x_values)} vs {len(y_values)}")
        if len(x_values) < 2:
            raise ArgumentError("Need at least 2 values to calculate covariance")

        # Single-pass algorithm
        n = 0
        mean_x = 0.0
        mean_y = 0.0
        c = 0.0  # Co-moment

        for x, y in zip(x_values, y_values):
            n += 1
            dx = x - mean_x
            mean_x += dx / n
            mean_y += (y - mean_y) / n
            c += dx * (y - mean_y)

        return Scalar(c / (n - 1))

    def _linear_regression(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x_values = self._extract_numbers(args[0], "x_values")
        y_values = self._extract_numbers(args[1], "y_values")

        if len(x_values) != len(y_values):
            raise ArgumentError(f"Lists must have same length: {len(x_values)} vs {len(y_values)}")
        if len(x_values) < 2:
            raise ArgumentError("Need at least 2 points for linear regression")

        # Single-pass algorithm for slope, intercept, and R-squared
        n = 0
        mean_x = 0.0
        mean_y = 0.0
        c = 0.0   # Co-moment (for covariance)
        m2_x = 0.0  # Sum of squared deviations for x
        m2_y = 0.0  # Sum of squared deviations for y

        for x, y in zip(x_values, y_values):
            n += 1
            dx = x - mean_x
            mean_x += dx / n
            dy = y - mean_y
            mean_y += dy / n
            # Update using corrected values
            c += dx * (y - mean_y)
            m2_x += dx * (x - mean_x)
            m2_y += dy * (y - mean_y)

        if m2_x == 0:
            raise ArgumentError("Cannot perform regression: all x values are identical")

        slope = c / m2_x
        intercept = mean_y - slope * mean_x

        # R-squared = correlation^2 = (cov / (std_x * std_y))^2 = c^2 / (m2_x * m2_y)
        r_squared = (c * c) / (m2_x * m2_y) if m2_y != 0 else 1.0

        return List([Scalar(slope), Scalar(intercept), Scalar(r_squared)])

    def _percentile_from_sorted(self, sorted_values: list[float], p: float) -> float:
        """Calculate the pth percentile from pre-sorted values using linear interpolation."""
        n = len(sorted_values)

        if p == 0:
            return sorted_values[0]
        if p == 100:
            return sorted_values[-1]

        # Linear interpolation
        idx = (p / 100) * (n - 1)
        lower = int(idx)
        upper = lower + 1

        if upper >= n:
            return sorted_values[-1]

        weight = idx - lower
        return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight

    def _percentile(self, args: list["MathObject"], session: "Session") -> "MathObject":
        values = self._extract_numbers(args[0])
        if not values:
            raise ArgumentError("Cannot calculate percentile of empty list")

        p_arg = args[1]
        if not isinstance(p_arg, Scalar):
            raise TypeError(f"Percentile must be a number, got {p_arg.type_name}")
        p = float(p_arg.value)

        if p < 0 or p > 100:
            raise ArgumentError(f"Percentile must be between 0 and 100, got {p}")

        sorted_values = sorted(values)
        return Scalar(self._percentile_from_sorted(sorted_values, p))

    def _quartiles(self, args: list["MathObject"], session: "Session") -> "MathObject":
        values = self._extract_numbers(args[0])
        if not values:
            raise ArgumentError("Cannot calculate quartiles of empty list")

        # Sort once, compute all quartiles
        sorted_values = sorted(values)
        q1 = self._percentile_from_sorted(sorted_values, 25)
        q2 = self._percentile_from_sorted(sorted_values, 50)
        q3 = self._percentile_from_sorted(sorted_values, 75)

        return List([Scalar(q1), Scalar(q2), Scalar(q3)])

    def _iqr(self, args: list["MathObject"], session: "Session") -> "MathObject":
        values = self._extract_numbers(args[0])
        if not values:
            raise ArgumentError("Cannot calculate IQR of empty list")

        # Sort once, compute both quartiles
        sorted_values = sorted(values)
        q1 = self._percentile_from_sorted(sorted_values, 25)
        q3 = self._percentile_from_sorted(sorted_values, 75)

        return Scalar(q3 - q1)
