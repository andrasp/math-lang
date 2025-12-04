"""Vector operations: Vector creation, DotProduct, CrossProduct, Magnitude, etc."""

import math
from typing import TYPE_CHECKING

from mathlang.operations.base import Operation, OperationProvider, ArgInfo
from mathlang.types.scalar import Scalar
from mathlang.types.vector import Vector
from mathlang.types.collection import List, Interval
from mathlang.engine.errors import TypeError, ArgumentError

if TYPE_CHECKING:
    from mathlang.types.base import MathObject
    from mathlang.engine.session import Session


class VectorsProvider(OperationProvider):
    """Provider for vector operations."""

    @property
    def name(self) -> str:
        return "Vectors"

    def _register_operations(self) -> None:
        self.register(Operation(
            identifier="Vec",
            friendly_name="Create Vector",
            description="Creates a vector from the given numeric arguments",
            category="Vectors/Creation",
            has_variable_args=True,
            variable_arg_info=ArgInfo("components", "Numeric components of the vector"),
            execute=self._vec,
        ))

        self.register(Operation(
            identifier="VecFromList",
            friendly_name="Vector from List",
            description="Creates a vector from a list of numbers",
            category="Vectors/Creation",
            required_args=[ArgInfo("list", "List of numeric values")],
            execute=self._vec_from_list,
        ))

        self.register(Operation(
            identifier="DotProduct",
            friendly_name="Dot Product",
            description="Calculates the dot product of two vectors",
            category="Vectors/Operations",
            required_args=[
                ArgInfo("v1", "First vector"),
                ArgInfo("v2", "Second vector"),
            ],
            execute=self._dot_product,
        ))

        self.register(Operation(
            identifier="CrossProduct",
            friendly_name="Cross Product",
            description="Calculates the cross product of two 3D vectors",
            category="Vectors/Operations",
            required_args=[
                ArgInfo("v1", "First 3D vector"),
                ArgInfo("v2", "Second 3D vector"),
            ],
            execute=self._cross_product,
        ))

        self.register(Operation(
            identifier="Magnitude",
            friendly_name="Magnitude",
            description="Calculates the magnitude (length) of a vector",
            category="Vectors/Properties",
            required_args=[ArgInfo("v", "The vector")],
            execute=self._magnitude,
        ))

        self.register(Operation(
            identifier="Normalize",
            friendly_name="Normalize",
            description="Returns the unit vector in the same direction",
            category="Vectors/Operations",
            required_args=[ArgInfo("v", "The vector to normalize")],
            execute=self._normalize,
        ))

        self.register(Operation(
            identifier="VecAngle",
            friendly_name="Angle Between Vectors",
            description="Calculates the angle between two vectors in radians",
            category="Vectors/Properties",
            required_args=[
                ArgInfo("v1", "First vector"),
                ArgInfo("v2", "Second vector"),
            ],
            execute=self._angle,
        ))

        self.register(Operation(
            identifier="VecAdd",
            friendly_name="Vector Addition",
            description="Adds two vectors element-wise",
            category="Vectors/Arithmetic",
            required_args=[
                ArgInfo("v1", "First vector"),
                ArgInfo("v2", "Second vector"),
            ],
            execute=self._vec_add,
        ))

        self.register(Operation(
            identifier="VecSub",
            friendly_name="Vector Subtraction",
            description="Subtracts the second vector from the first",
            category="Vectors/Arithmetic",
            required_args=[
                ArgInfo("v1", "First vector"),
                ArgInfo("v2", "Second vector"),
            ],
            execute=self._vec_sub,
        ))

        self.register(Operation(
            identifier="VecScale",
            friendly_name="Vector Scaling",
            description="Multiplies a vector by a scalar",
            category="Vectors/Arithmetic",
            required_args=[
                ArgInfo("v", "The vector"),
                ArgInfo("scalar", "The scalar to multiply by"),
            ],
            execute=self._vec_scale,
        ))

        self.register(Operation(
            identifier="VecDim",
            friendly_name="Vector Dimension",
            description="Returns the dimension (number of components) of a vector",
            category="Vectors/Properties",
            required_args=[ArgInfo("v", "The vector")],
            execute=self._vec_dim,
        ))

        self.register(Operation(
            identifier="VecComponent",
            friendly_name="Vector Component",
            description="Gets a specific component of a vector (0-indexed)",
            category="Vectors/Access",
            required_args=[
                ArgInfo("v", "The vector"),
                ArgInfo("index", "Component index (0-based)"),
            ],
            execute=self._vec_component,
        ))

        self.register(Operation(
            identifier="ZeroVec",
            friendly_name="Zero Vector",
            description="Creates a zero vector of specified dimension",
            category="Vectors/Creation",
            required_args=[ArgInfo("dim", "Dimension of the vector")],
            execute=self._zero_vec,
        ))

        self.register(Operation(
            identifier="UnitVec",
            friendly_name="Unit Vector",
            description="Creates a unit vector along a specified axis",
            category="Vectors/Creation",
            required_args=[
                ArgInfo("dim", "Dimension of the vector"),
                ArgInfo("axis", "Axis index (0-based)"),
            ],
            execute=self._unit_vec,
        ))

        self.register(Operation(
            identifier="Projection",
            friendly_name="Vector Projection",
            description="Projects vector v1 onto vector v2",
            category="Vectors/Operations",
            required_args=[
                ArgInfo("v1", "Vector to project"),
                ArgInfo("v2", "Vector to project onto"),
            ],
            execute=self._projection,
        ))

    def _extract_vector(self, value: "MathObject", name: str) -> list[float]:
        """Extract numeric components from a Vector, List, or Interval."""
        if isinstance(value, Vector):
            return [float(v) for v in value.values]
        if isinstance(value, Interval):
            # Interval contains only numbers, use optimized to_list()
            return value.to_list()
        if isinstance(value, List):
            result = []
            for item in value:
                if not isinstance(item, Scalar) or isinstance(item.value, str):
                    raise TypeError(f"{name} must contain only numbers")
                result.append(float(item.value))
            return result
        raise TypeError(f"{name} must be a vector, list, or interval, got {value.type_name}")

    def _vec(self, args: list["MathObject"], session: "Session") -> "MathObject":
        values = []
        for arg in args:
            if not isinstance(arg, Scalar) or isinstance(arg.value, str):
                raise TypeError(f"Vector components must be numeric, got {arg.type_name}")
            values.append(arg.value)
        return Vector(values)

    def _vec_from_list(self, args: list["MathObject"], session: "Session") -> "MathObject":
        components = self._extract_vector(args[0], "list")
        return Vector(components)

    def _dot_product(self, args: list["MathObject"], session: "Session") -> "MathObject":
        v1 = self._extract_vector(args[0], "v1")
        v2 = self._extract_vector(args[1], "v2")

        if len(v1) != len(v2):
            raise ArgumentError(f"Vectors must have same dimension: {len(v1)} vs {len(v2)}")

        return Scalar(sum(a * b for a, b in zip(v1, v2)))

    def _cross_product(self, args: list["MathObject"], session: "Session") -> "MathObject":
        v1 = self._extract_vector(args[0], "v1")
        v2 = self._extract_vector(args[1], "v2")

        if len(v1) != 3 or len(v2) != 3:
            raise ArgumentError("Cross product requires 3D vectors")

        result = [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0],
        ]
        return Vector(result)

    def _magnitude(self, args: list["MathObject"], session: "Session") -> "MathObject":
        v = self._extract_vector(args[0], "v")
        return Scalar(math.sqrt(sum(x * x for x in v)))

    def _normalize(self, args: list["MathObject"], session: "Session") -> "MathObject":
        v = self._extract_vector(args[0], "v")
        mag = math.sqrt(sum(x * x for x in v))

        if mag == 0:
            raise ArgumentError("Cannot normalize zero vector")

        return Vector([x / mag for x in v])

    def _angle(self, args: list["MathObject"], session: "Session") -> "MathObject":
        v1 = self._extract_vector(args[0], "v1")
        v2 = self._extract_vector(args[1], "v2")

        if len(v1) != len(v2):
            raise ArgumentError(f"Vectors must have same dimension: {len(v1)} vs {len(v2)}")

        dot = sum(a * b for a, b in zip(v1, v2))
        mag1 = math.sqrt(sum(x * x for x in v1))
        mag2 = math.sqrt(sum(x * x for x in v2))

        if mag1 == 0 or mag2 == 0:
            raise ArgumentError("Cannot calculate angle with zero vector")

        cos_angle = dot / (mag1 * mag2)
        # Clamp to handle floating point errors
        cos_angle = max(-1, min(1, cos_angle))
        return Scalar(math.acos(cos_angle))

    def _vec_add(self, args: list["MathObject"], session: "Session") -> "MathObject":
        v1 = self._extract_vector(args[0], "v1")
        v2 = self._extract_vector(args[1], "v2")

        if len(v1) != len(v2):
            raise ArgumentError(f"Vectors must have same dimension: {len(v1)} vs {len(v2)}")

        return Vector([a + b for a, b in zip(v1, v2)])

    def _vec_sub(self, args: list["MathObject"], session: "Session") -> "MathObject":
        v1 = self._extract_vector(args[0], "v1")
        v2 = self._extract_vector(args[1], "v2")

        if len(v1) != len(v2):
            raise ArgumentError(f"Vectors must have same dimension: {len(v1)} vs {len(v2)}")

        return Vector([a - b for a, b in zip(v1, v2)])

    def _vec_scale(self, args: list["MathObject"], session: "Session") -> "MathObject":
        v = self._extract_vector(args[0], "v")
        scalar = args[1]

        if not isinstance(scalar, Scalar) or isinstance(scalar.value, str):
            raise TypeError(f"Scalar must be numeric, got {scalar.type_name}")

        s = float(scalar.value)
        return Vector([x * s for x in v])

    def _vec_dim(self, args: list["MathObject"], session: "Session") -> "MathObject":
        v = self._extract_vector(args[0], "v")
        return Scalar(len(v))

    def _vec_component(self, args: list["MathObject"], session: "Session") -> "MathObject":
        v = self._extract_vector(args[0], "v")
        index_arg = args[1]

        if not isinstance(index_arg, Scalar) or not isinstance(index_arg.value, int):
            raise TypeError(f"Index must be an integer, got {index_arg.type_name}")

        index = index_arg.value
        if index < 0 or index >= len(v):
            raise ArgumentError(f"Index {index} out of range for vector of dimension {len(v)}")

        return Scalar(v[index])

    def _zero_vec(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dim_arg = args[0]

        if not isinstance(dim_arg, Scalar) or not isinstance(dim_arg.value, int):
            raise TypeError(f"Dimension must be an integer, got {dim_arg.type_name}")

        dim = dim_arg.value
        if dim <= 0:
            raise ArgumentError(f"Dimension must be positive, got {dim}")

        return Vector([0.0] * dim)

    def _unit_vec(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dim_arg = args[0]
        axis_arg = args[1]

        if not isinstance(dim_arg, Scalar) or not isinstance(dim_arg.value, int):
            raise TypeError(f"Dimension must be an integer, got {dim_arg.type_name}")
        if not isinstance(axis_arg, Scalar) or not isinstance(axis_arg.value, int):
            raise TypeError(f"Axis must be an integer, got {axis_arg.type_name}")

        dim = dim_arg.value
        axis = axis_arg.value

        if dim <= 0:
            raise ArgumentError(f"Dimension must be positive, got {dim}")
        if axis < 0 or axis >= dim:
            raise ArgumentError(f"Axis {axis} out of range for dimension {dim}")

        result = [0.0] * dim
        result[axis] = 1.0
        return Vector(result)

    def _projection(self, args: list["MathObject"], session: "Session") -> "MathObject":
        v1 = self._extract_vector(args[0], "v1")
        v2 = self._extract_vector(args[1], "v2")

        if len(v1) != len(v2):
            raise ArgumentError(f"Vectors must have same dimension: {len(v1)} vs {len(v2)}")

        dot_v1_v2 = sum(a * b for a, b in zip(v1, v2))
        dot_v2_v2 = sum(x * x for x in v2)

        if dot_v2_v2 == 0:
            raise ArgumentError("Cannot project onto zero vector")

        scale = dot_v1_v2 / dot_v2_v2
        return Vector([x * scale for x in v2])
