"""Visualization operations: Plot, Plot3D, Histogram, Scatter."""

from typing import TYPE_CHECKING

from mathlang.operations.base import Operation, OperationProvider, ArgInfo
from mathlang.types.scalar import Scalar
from mathlang.types.collection import List
from mathlang.types.callable import Lambda
from mathlang.types.result import PlotData2D, PlotData3D, HistogramData, ScatterData
from mathlang.engine.errors import TypeError, ArgumentError

if TYPE_CHECKING:
    from mathlang.types.base import MathObject
    from mathlang.engine.session import Session


class VisualizationProvider(OperationProvider):
    """Provider for visualization operations."""

    @property
    def name(self) -> str:
        return "Visualization"

    def _register_operations(self) -> None:
        self.register(Operation(
            identifier="Plot",
            friendly_name="Plot 2D",
            description="Creates a 2D plot from a function or data points",
            category="Visualization/2D",
            required_args=[ArgInfo("func_or_x", "Lambda function or x values")],
            optional_args=[
                ArgInfo("x_min_or_y", "X minimum (for function) or y values (for data)", default=None),
                ArgInfo("x_max", "X maximum (for function)", default=None),
                ArgInfo("points", "Number of points to plot", default=100),
            ],
            execute=self._plot,
        ))

        self.register(Operation(
            identifier="PlotData",
            friendly_name="Plot Data Points",
            description="Creates a 2D plot from x and y data lists",
            category="Visualization/2D",
            required_args=[
                ArgInfo("x_values", "List of x values"),
                ArgInfo("y_values", "List of y values"),
            ],
            optional_args=[
                ArgInfo("title", "Plot title", default=""),
            ],
            execute=self._plot_data,
        ))

        self.register(Operation(
            identifier="Plot3D",
            friendly_name="Plot 3D Surface",
            description="Creates a 3D surface plot from a function",
            category="Visualization/3D",
            required_args=[
                ArgInfo("func", "Lambda function f(x, y)"),
                ArgInfo("x_min", "X minimum"),
                ArgInfo("x_max", "X maximum"),
                ArgInfo("y_min", "Y minimum"),
                ArgInfo("y_max", "Y maximum"),
            ],
            optional_args=[
                ArgInfo("points", "Number of points per axis", default=30),
            ],
            execute=self._plot3d,
        ))

        self.register(Operation(
            identifier="Histogram",
            friendly_name="Histogram",
            description="Creates a histogram from data",
            category="Visualization/Statistical",
            required_args=[ArgInfo("data", "List of numeric values")],
            optional_args=[
                ArgInfo("bins", "Number of bins", default=10),
                ArgInfo("title", "Plot title", default=""),
            ],
            execute=self._histogram,
        ))

        self.register(Operation(
            identifier="Scatter",
            friendly_name="Scatter Plot",
            description="Creates a scatter plot from x and y data",
            category="Visualization/2D",
            required_args=[
                ArgInfo("x_values", "List of x values"),
                ArgInfo("y_values", "List of y values"),
            ],
            optional_args=[
                ArgInfo("title", "Plot title", default=""),
            ],
            execute=self._scatter,
        ))

        self.register(Operation(
            identifier="LinePlot",
            friendly_name="Line Plot",
            description="Creates a line plot connecting data points",
            category="Visualization/2D",
            required_args=[
                ArgInfo("x_values", "List of x values"),
                ArgInfo("y_values", "List of y values"),
            ],
            optional_args=[
                ArgInfo("title", "Plot title", default=""),
            ],
            execute=self._line_plot,
        ))

        self.register(Operation(
            identifier="MultiPlot",
            friendly_name="Multiple Plots",
            description="Creates multiple function plots on the same axes",
            category="Visualization/2D",
            required_args=[
                ArgInfo("functions", "List of lambda functions"),
                ArgInfo("x_min", "X minimum"),
                ArgInfo("x_max", "X maximum"),
            ],
            optional_args=[
                ArgInfo("points", "Number of points", default=100),
            ],
            execute=self._multi_plot,
        ))

    def _extract_list(self, value: "MathObject", name: str) -> list[float]:
        """Extract a list of floats from a MathObject."""
        if not isinstance(value, List):
            raise TypeError(f"{name} must be a list, got {value.type_name}")

        result = []
        for item in value:
            if not isinstance(item, Scalar) or isinstance(item.value, str):
                raise TypeError(f"{name} must contain only numbers")
            result.append(float(item.value))
        return result

    def _get_number(self, value: "MathObject", name: str) -> float:
        """Extract a number from a MathObject."""
        if not isinstance(value, Scalar) or isinstance(value.value, str):
            raise TypeError(f"{name} must be a number, got {value.type_name}")
        return float(value.value)

    def _get_int(self, value: "MathObject", name: str) -> int:
        """Extract an integer from a MathObject."""
        if not isinstance(value, Scalar) or not isinstance(value.value, int):
            raise TypeError(f"{name} must be an integer, got {value.type_name}")
        return value.value

    def _get_string(self, value: "MathObject", name: str, default: str = "") -> str:
        """Extract a string from a MathObject."""
        if value is None:
            return default
        if isinstance(value, Scalar) and isinstance(value.value, str):
            return value.value
        return default

    def _evaluate_function(self, func: Lambda, x: float, session: "Session") -> float:
        """Evaluate a single-argument lambda at x."""
        from mathlang.engine.evaluator import evaluate_expression

        if func.arity != 1:
            raise ArgumentError(f"Plot function must take 1 argument, got {func.arity}")

        child = session.create_child()
        child.set(func.parameters[0], Scalar(x))
        result = evaluate_expression(func.body, child)

        if not isinstance(result, Scalar) or isinstance(result.value, str):
            raise TypeError(f"Function must return a number, got {result.type_name}")
        return float(result.value)

    def _evaluate_function_2d(self, func: Lambda, x: float, y: float, session: "Session") -> float:
        """Evaluate a two-argument lambda at (x, y)."""
        from mathlang.engine.evaluator import evaluate_expression

        if func.arity != 2:
            raise ArgumentError(f"3D plot function must take 2 arguments, got {func.arity}")

        child = session.create_child()
        child.set(func.parameters[0], Scalar(x))
        child.set(func.parameters[1], Scalar(y))
        result = evaluate_expression(func.body, child)

        if not isinstance(result, Scalar) or isinstance(result.value, str):
            raise TypeError(f"Function must return a number, got {result.type_name}")
        return float(result.value)

    def _plot(self, args: list["MathObject"], session: "Session") -> "MathObject":
        first_arg = args[0]

        # Check if it's a function plot or data plot
        if isinstance(first_arg, Lambda):
            # Function plot: Plot(f, x_min, x_max, points?)
            func = first_arg
            if len(args) < 3:
                raise ArgumentError("Plot with function requires x_min and x_max")

            x_min = self._get_number(args[1], "x_min")
            x_max = self._get_number(args[2], "x_max")
            points = self._get_int(args[3], "points") if len(args) > 3 else 100

            if x_min >= x_max:
                raise ArgumentError(f"x_min ({x_min}) must be less than x_max ({x_max})")
            if points < 2:
                raise ArgumentError("Need at least 2 points")

            step = (x_max - x_min) / (points - 1)
            x_values = [x_min + i * step for i in range(points)]
            y_values = []

            for x in x_values:
                try:
                    y = self._evaluate_function(func, x, session)
                    y_values.append(y)
                except Exception:
                    y_values.append(float('nan'))

            return PlotData2D(x_values=x_values, y_values=y_values)

        elif isinstance(first_arg, List):
            # Data plot: Plot(x_values, y_values)
            if len(args) < 2 or not isinstance(args[1], List):
                raise ArgumentError("Plot with data requires x_values and y_values lists")

            x_values = self._extract_list(first_arg, "x_values")
            y_values = self._extract_list(args[1], "y_values")

            if len(x_values) != len(y_values):
                raise ArgumentError(f"x and y must have same length: {len(x_values)} vs {len(y_values)}")

            return PlotData2D(x_values=x_values, y_values=y_values)

        else:
            raise TypeError(f"Plot expects a function or list, got {first_arg.type_name}")

    def _plot_data(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x_values = self._extract_list(args[0], "x_values")
        y_values = self._extract_list(args[1], "y_values")
        title = self._get_string(args[2] if len(args) > 2 else None, "title")

        if len(x_values) != len(y_values):
            raise ArgumentError(f"x and y must have same length: {len(x_values)} vs {len(y_values)}")

        return PlotData2D(x_values=x_values, y_values=y_values, title=title)

    def _plot3d(self, args: list["MathObject"], session: "Session") -> "MathObject":
        func = args[0]
        if not isinstance(func, Lambda):
            raise TypeError(f"Plot3D expects a function, got {func.type_name}")

        x_min = self._get_number(args[1], "x_min")
        x_max = self._get_number(args[2], "x_max")
        y_min = self._get_number(args[3], "y_min")
        y_max = self._get_number(args[4], "y_max")
        points = self._get_int(args[5], "points") if len(args) > 5 else 30

        if x_min >= x_max:
            raise ArgumentError(f"x_min ({x_min}) must be less than x_max ({x_max})")
        if y_min >= y_max:
            raise ArgumentError(f"y_min ({y_min}) must be less than y_max ({y_max})")
        if points < 2:
            raise ArgumentError("Need at least 2 points")

        x_step = (x_max - x_min) / (points - 1)
        y_step = (y_max - y_min) / (points - 1)

        x_values = [x_min + i * x_step for i in range(points)]
        y_values = [y_min + i * y_step for i in range(points)]
        z_values = []

        for y in y_values:
            z_row = []
            for x in x_values:
                try:
                    z = self._evaluate_function_2d(func, x, y, session)
                    z_row.append(z)
                except Exception:
                    z_row.append(float('nan'))
            z_values.append(z_row)

        return PlotData3D(x_values=x_values, y_values=y_values, z_values=z_values)

    def _histogram(self, args: list["MathObject"], session: "Session") -> "MathObject":
        values = self._extract_list(args[0], "data")
        bins = self._get_int(args[1], "bins") if len(args) > 1 else 10
        title = self._get_string(args[2] if len(args) > 2 else None, "title")

        if bins < 1:
            raise ArgumentError("bins must be positive")
        if not values:
            raise ArgumentError("data cannot be empty")

        return HistogramData(values=values, bins=bins, title=title)

    def _scatter(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x_values = self._extract_list(args[0], "x_values")
        y_values = self._extract_list(args[1], "y_values")
        title = self._get_string(args[2] if len(args) > 2 else None, "title")

        if len(x_values) != len(y_values):
            raise ArgumentError(f"x and y must have same length: {len(x_values)} vs {len(y_values)}")

        return ScatterData(x_values=x_values, y_values=y_values, title=title)

    def _line_plot(self, args: list["MathObject"], session: "Session") -> "MathObject":
        x_values = self._extract_list(args[0], "x_values")
        y_values = self._extract_list(args[1], "y_values")
        title = self._get_string(args[2] if len(args) > 2 else None, "title")

        if len(x_values) != len(y_values):
            raise ArgumentError(f"x and y must have same length: {len(x_values)} vs {len(y_values)}")

        return PlotData2D(x_values=x_values, y_values=y_values, title=title)

    def _multi_plot(self, args: list["MathObject"], session: "Session") -> "MathObject":
        """Create multiple plots - returns a list of PlotData2D objects."""
        functions = args[0]
        if not isinstance(functions, List):
            raise TypeError(f"functions must be a list, got {functions.type_name}")

        x_min = self._get_number(args[1], "x_min")
        x_max = self._get_number(args[2], "x_max")
        points = self._get_int(args[3], "points") if len(args) > 3 else 100

        if x_min >= x_max:
            raise ArgumentError(f"x_min ({x_min}) must be less than x_max ({x_max})")

        step = (x_max - x_min) / (points - 1)
        x_values = [x_min + i * step for i in range(points)]

        plots = []
        for func in functions:
            if not isinstance(func, Lambda):
                raise TypeError(f"Each function must be a lambda, got {func.type_name}")

            y_values = []
            for x in x_values:
                try:
                    y = self._evaluate_function(func, x, session)
                    y_values.append(y)
                except Exception:
                    y_values.append(float('nan'))

            plots.append(PlotData2D(x_values=x_values, y_values=y_values))

        return List(plots)
