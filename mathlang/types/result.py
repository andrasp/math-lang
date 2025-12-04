"""Result types: PlotData, Error, Notification."""

from dataclasses import dataclass

from mathlang.types.base import MathObject


@dataclass
class PlotData2D(MathObject):
    """2D plot data for visualization."""

    x_values: list[float]
    y_values: list[float]
    title: str = ""
    x_label: str = "x"
    y_label: str = "y"

    @property
    def type_name(self) -> str:
        return "PlotData2D"

    def __repr__(self) -> str:
        return f"PlotData2D({len(self.x_values)} points)"

    def display(self) -> str:
        return f"[Plot: {len(self.x_values)} points]"

    def to_dict(self) -> dict:
        """Serialize to dictionary for JSON transmission."""
        return {
            "type": "PlotData2D",
            "x_values": self.x_values,
            "y_values": self.y_values,
            "title": self.title,
            "x_label": self.x_label,
            "y_label": self.y_label,
        }


@dataclass
class PlotData3D(MathObject):
    """3D plot data for visualization."""

    x_values: list[float]
    y_values: list[float]
    z_values: list[list[float]]
    title: str = ""
    x_label: str = "x"
    y_label: str = "y"
    z_label: str = "z"

    @property
    def type_name(self) -> str:
        return "PlotData3D"

    def __repr__(self) -> str:
        return f"PlotData3D({len(self.x_values)}x{len(self.y_values)} grid)"

    def display(self) -> str:
        return f"[3D Plot: {len(self.x_values)}x{len(self.y_values)} grid]"

    def to_dict(self) -> dict:
        """Serialize to dictionary for JSON transmission."""
        return {
            "type": "PlotData3D",
            "x_values": self.x_values,
            "y_values": self.y_values,
            "z_values": self.z_values,
            "title": self.title,
            "x_label": self.x_label,
            "y_label": self.y_label,
            "z_label": self.z_label,
        }


@dataclass
class HistogramData(MathObject):
    """Histogram data for visualization."""

    values: list[float]
    bins: int = 10
    title: str = ""
    x_label: str = "Value"
    y_label: str = "Frequency"

    @property
    def type_name(self) -> str:
        return "HistogramData"

    def __repr__(self) -> str:
        return f"HistogramData({len(self.values)} values, {self.bins} bins)"

    def display(self) -> str:
        return f"[Histogram: {len(self.values)} values, {self.bins} bins]"


@dataclass
class ScatterData(MathObject):
    """Scatter plot data for visualization."""

    x_values: list[float]
    y_values: list[float]
    title: str = ""
    x_label: str = "x"
    y_label: str = "y"

    @property
    def type_name(self) -> str:
        return "ScatterData"

    def __repr__(self) -> str:
        return f"ScatterData({len(self.x_values)} points)"

    def display(self) -> str:
        return f"[Scatter: {len(self.x_values)} points]"


@dataclass
class Error(MathObject):
    """An error result."""

    message: str
    details: str = ""

    @property
    def type_name(self) -> str:
        return "Error"

    def __repr__(self) -> str:
        return f"Error({self.message!r})"

    def display(self) -> str:
        if self.details:
            return f"Error: {self.message}\n{self.details}"
        return f"Error: {self.message}"


@dataclass
class Notification(MathObject):
    """A success/info notification."""

    message: str

    @property
    def type_name(self) -> str:
        return "Notification"

    def __repr__(self) -> str:
        return f"Notification({self.message!r})"

    def display(self) -> str:
        return self.message
