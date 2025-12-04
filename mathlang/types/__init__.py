"""Type system for MathLang values."""

from mathlang.types.base import MathObject
from mathlang.types.scalar import Scalar
from mathlang.types.vector import Vector
from mathlang.types.collection import List, Interval
from mathlang.types.callable import Lambda
from mathlang.types.result import PlotData2D, PlotData3D, Error, Notification

__all__ = [
    "MathObject",
    "Scalar",
    "Vector",
    "List",
    "Interval",
    "Lambda",
    "PlotData2D",
    "PlotData3D",
    "Error",
    "Notification",
]
