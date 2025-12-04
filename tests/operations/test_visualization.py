"""Tests for visualization operations."""

import pytest

from mathlang.engine import evaluate
from mathlang.types.scalar import Scalar
from mathlang.types.result import PlotData2D, PlotData3D, HistogramData, ScatterData


class TestPlot:
    """Tests for Plot function."""

    def test_plot_with_function(self, session):
        results = evaluate("Plot(x -> x^2, -1, 1, 10)", session)
        result = results[0].value
        assert isinstance(result, PlotData2D)
        assert len(result.x_values) == 10
        assert len(result.y_values) == 10
        assert result.y_values[0] == pytest.approx(1.0)

    def test_plot_with_lists(self, session):
        results = evaluate("Plot(List(1, 2, 3), List(1, 4, 9))", session)
        result = results[0].value
        assert isinstance(result, PlotData2D)
        assert result.x_values == [1.0, 2.0, 3.0]
        assert result.y_values == [1.0, 4.0, 9.0]

    def test_plot_function_requires_range(self, session):
        from mathlang.engine.errors import ArgumentError
        with pytest.raises(ArgumentError, match="requires x_min and x_max"):
            evaluate("Plot(x -> x^2, 1)", session)

    def test_plot_invalid_range(self, session):
        from mathlang.engine.errors import ArgumentError
        with pytest.raises(ArgumentError, match="x_min.*must be less than x_max"):
            evaluate("Plot(x -> x, 5, 1)", session)

    def test_plot_needs_at_least_2_points(self, session):
        from mathlang.engine.errors import ArgumentError
        with pytest.raises(ArgumentError, match="at least 2 points"):
            evaluate("Plot(x -> x, 0, 1, 1)", session)

    def test_plot_mismatched_list_lengths(self, session):
        from mathlang.engine.errors import ArgumentError
        with pytest.raises(ArgumentError, match="same length"):
            evaluate("Plot(List(1, 2, 3), List(1, 2))", session)

    def test_plot_with_invalid_first_arg(self, session):
        from mathlang.engine.errors import TypeError
        with pytest.raises(TypeError, match="expects a function or list"):
            evaluate("Plot(5, 0, 1)", session)


class TestPlotData:
    """Tests for PlotData function."""

    def test_plot_data_basic(self, session):
        results = evaluate("PlotData(List(1, 2, 3), List(4, 5, 6))", session)
        result = results[0].value
        assert isinstance(result, PlotData2D)
        assert result.x_values == [1.0, 2.0, 3.0]
        assert result.y_values == [4.0, 5.0, 6.0]

    def test_plot_data_with_title(self, session):
        results = evaluate('PlotData(List(1, 2), List(3, 4), "My Plot")', session)
        result = results[0].value
        assert result.title == "My Plot"

    def test_plot_data_mismatched_lengths(self, session):
        from mathlang.engine.errors import ArgumentError
        with pytest.raises(ArgumentError, match="same length"):
            evaluate("PlotData(List(1, 2, 3), List(1))", session)


class TestPlot3D:
    """Tests for Plot3D function."""

    def test_plot3d_basic(self, session):
        results = evaluate("Plot3D((x, y) -> x + y, -1, 1, -1, 1, 5)", session)
        result = results[0].value
        assert isinstance(result, PlotData3D)
        assert len(result.x_values) == 5
        assert len(result.y_values) == 5
        assert len(result.z_values) == 5
        assert len(result.z_values[0]) == 5

    def test_plot3d_default_points(self, session):
        results = evaluate("Plot3D((x, y) -> x * y, 0, 1, 0, 1)", session)
        result = results[0].value
        assert len(result.x_values) == 30

    def test_plot3d_invalid_x_range(self, session):
        from mathlang.engine.errors import ArgumentError
        with pytest.raises(ArgumentError, match="x_min.*must be less than x_max"):
            evaluate("Plot3D((x, y) -> x, 1, 0, -1, 1)", session)

    def test_plot3d_invalid_y_range(self, session):
        from mathlang.engine.errors import ArgumentError
        with pytest.raises(ArgumentError, match="y_min.*must be less than y_max"):
            evaluate("Plot3D((x, y) -> x, 0, 1, 1, 0)", session)

    def test_plot3d_needs_2_args_function(self, session):
        # Plot3D catches exceptions and returns NaN, so it doesn't raise
        # The error is caught in _evaluate_function_2d but wrapped
        results = evaluate("Plot3D(x -> x, 0, 1, 0, 1, 3)", session)
        result = results[0].value
        # All values should be NaN since the function has wrong arity
        import math
        assert all(math.isnan(z) for row in result.z_values for z in row)

    def test_plot3d_not_function(self, session):
        from mathlang.engine.errors import TypeError
        with pytest.raises(TypeError, match="expects a function"):
            evaluate("Plot3D(5, 0, 1, 0, 1)", session)


class TestHistogram:
    """Tests for Histogram function."""

    def test_histogram_basic(self, session):
        results = evaluate("Histogram(List(1, 2, 2, 3, 3, 3))", session)
        result = results[0].value
        assert isinstance(result, HistogramData)
        assert result.values == [1.0, 2.0, 2.0, 3.0, 3.0, 3.0]
        assert result.bins == 10

    def test_histogram_with_bins(self, session):
        results = evaluate("Histogram(List(1, 2, 3, 4, 5), 5)", session)
        result = results[0].value
        assert result.bins == 5

    def test_histogram_with_title(self, session):
        results = evaluate('Histogram(List(1, 2, 3), 10, "My Histogram")', session)
        result = results[0].value
        assert result.title == "My Histogram"

    def test_histogram_invalid_bins(self, session):
        from mathlang.engine.errors import ArgumentError
        with pytest.raises(ArgumentError, match="bins must be positive"):
            evaluate("Histogram(List(1, 2, 3), 0)", session)

    def test_histogram_empty_data(self, session):
        from mathlang.engine.errors import ArgumentError
        with pytest.raises(ArgumentError, match="cannot be empty"):
            evaluate("Histogram(List())", session)


class TestScatter:
    """Tests for Scatter function."""

    def test_scatter_basic(self, session):
        results = evaluate("Scatter(List(1, 2, 3), List(4, 5, 6))", session)
        result = results[0].value
        assert isinstance(result, ScatterData)
        assert result.x_values == [1.0, 2.0, 3.0]
        assert result.y_values == [4.0, 5.0, 6.0]

    def test_scatter_with_title(self, session):
        results = evaluate('Scatter(List(1, 2), List(3, 4), "Points")', session)
        result = results[0].value
        assert result.title == "Points"

    def test_scatter_mismatched_lengths(self, session):
        from mathlang.engine.errors import ArgumentError
        with pytest.raises(ArgumentError, match="same length"):
            evaluate("Scatter(List(1, 2, 3), List(1))", session)


class TestLinePlot:
    """Tests for LinePlot function."""

    def test_line_plot_basic(self, session):
        results = evaluate("LinePlot(List(1, 2, 3), List(1, 4, 9))", session)
        result = results[0].value
        assert isinstance(result, PlotData2D)
        assert result.x_values == [1.0, 2.0, 3.0]
        assert result.y_values == [1.0, 4.0, 9.0]

    def test_line_plot_with_title(self, session):
        results = evaluate('LinePlot(List(0, 1), List(0, 1), "Line")', session)
        result = results[0].value
        assert result.title == "Line"


class TestMultiPlot:
    """Tests for MultiPlot function."""

    def test_multi_plot_basic(self, session):
        results = evaluate("MultiPlot(List(x -> x, x -> x^2), 0, 1, 5)", session)
        result = results[0].value
        assert len(result) == 2
        assert all(isinstance(p, PlotData2D) for p in result)

    def test_multi_plot_default_points(self, session):
        results = evaluate("MultiPlot(List(x -> x), 0, 1)", session)
        result = results[0].value
        assert len(result[0].x_values) == 100

    def test_multi_plot_invalid_range(self, session):
        from mathlang.engine.errors import ArgumentError
        with pytest.raises(ArgumentError, match="x_min.*must be less than x_max"):
            evaluate("MultiPlot(List(x -> x), 1, 0)", session)

    def test_multi_plot_not_list(self, session):
        from mathlang.engine.errors import TypeError
        with pytest.raises(TypeError, match="must be a list"):
            evaluate("MultiPlot(x -> x, 0, 1)", session)

    def test_multi_plot_contains_non_lambda(self, session):
        from mathlang.engine.errors import TypeError
        with pytest.raises(TypeError, match="Each function must be a lambda"):
            evaluate("MultiPlot(List(5), 0, 1)", session)


class TestHelperMethods:
    """Tests for visualization helper methods via edge cases."""

    def test_extract_list_non_numeric(self, session):
        from mathlang.engine.errors import TypeError
        with pytest.raises(TypeError, match="must contain only numbers"):
            evaluate('Scatter(List("a", "b"), List(1, 2))', session)

    def test_extract_list_not_list(self, session):
        from mathlang.engine.errors import TypeError
        with pytest.raises(TypeError, match="must be a list"):
            evaluate("Scatter(5, List(1, 2))", session)

    def test_get_number_non_numeric(self, session):
        from mathlang.engine.errors import TypeError
        with pytest.raises(TypeError, match="must be a number"):
            evaluate('Plot(x -> x, "a", 1)', session)

    def test_get_int_non_int(self, session):
        from mathlang.engine.errors import TypeError
        with pytest.raises(TypeError, match="must be an integer"):
            evaluate("Plot(x -> x, 0, 1, 5.5)", session)

    def test_function_returns_non_number(self, session):
        # Plot catches exceptions and returns NaN, so it doesn't raise
        results = evaluate('Plot(x -> "hello", 0, 1, 5)', session)
        result = results[0].value
        import math
        assert all(math.isnan(y) for y in result.y_values)

    def test_function_wrong_arity(self, session):
        # Plot catches exceptions and returns NaN, so it doesn't raise
        results = evaluate("Plot((x, y) -> x + y, 0, 1, 5)", session)
        result = results[0].value
        import math
        assert all(math.isnan(y) for y in result.y_values)
