"""Collection operations: List, Map, Reduce, Filter, etc."""

from typing import TYPE_CHECKING

from mathlang.operations.base import Operation, OperationProvider, ArgInfo
from mathlang.types.scalar import Scalar
from mathlang.types.collection import List, Interval
from mathlang.types.callable import Lambda
from mathlang.engine.errors import TypeError, ArgumentError

if TYPE_CHECKING:
    from mathlang.types.base import MathObject
    from mathlang.engine.session import Session


def _is_collection(obj: "MathObject") -> bool:
    """Check if an object is a collection (List or Interval)."""
    return isinstance(obj, (List, Interval))


class ListsProvider(OperationProvider):
    """Provider for collection operations."""

    @property
    def name(self) -> str:
        return "Collections"

    def _register_operations(self) -> None:
        self.register(Operation(
            identifier="List",
            friendly_name="Create List",
            description="Creates a list from the given arguments",
            category="Collections/Creation",
            has_variable_args=True,
            variable_arg_info=ArgInfo("items", "Items to include in the list"),
            execute=self._list,
        ))

        self.register(Operation(
            identifier="Range",
            friendly_name="Create Range",
            description="Creates an interval from start to end (exclusive)",
            category="Collections/Creation",
            required_args=[
                ArgInfo("start", "Start value"),
                ArgInfo("end", "End value (exclusive)"),
            ],
            optional_args=[ArgInfo("step", "Step value", default=1)],
            execute=self._range,
        ))

        self.register(Operation(
            identifier="Length",
            friendly_name="Length",
            description="Returns the length of a collection or string",
            category="Collections/Info",
            required_args=[ArgInfo("collection", "Collection or string")],
            execute=self._length,
        ))

        self.register(Operation(
            identifier="Map",
            friendly_name="Map",
            description="Applies a function to each element of a collection",
            category="Collections/Transform",
            required_args=[
                ArgInfo("collection", "The collection to map over"),
                ArgInfo("func", "Function to apply (lambda)"),
            ],
            execute=self._map,
        ))

        self.register(Operation(
            identifier="Filter",
            friendly_name="Filter",
            description="Filters a collection based on a predicate function",
            category="Collections/Transform",
            required_args=[
                ArgInfo("collection", "The collection to filter"),
                ArgInfo("predicate", "Function returning true/false (lambda)"),
            ],
            execute=self._filter,
        ))

        self.register(Operation(
            identifier="Reduce",
            friendly_name="Reduce",
            description="Reduces a collection to a single value using an accumulator function",
            category="Collections/Transform",
            required_args=[
                ArgInfo("collection", "The collection to reduce"),
                ArgInfo("func", "Function taking (accumulator, item) (lambda)"),
                ArgInfo("initial", "Initial accumulator value"),
            ],
            execute=self._reduce,
        ))

        self.register(Operation(
            identifier="Sum",
            friendly_name="Sum",
            description="Returns the sum of all elements in a collection",
            category="Collections/Aggregate",
            required_args=[ArgInfo("collection", "Collection of numbers")],
            execute=self._sum,
        ))

        self.register(Operation(
            identifier="Avg",
            friendly_name="Average",
            description="Returns the average of all elements in a collection",
            category="Collections/Aggregate",
            required_args=[ArgInfo("collection", "Collection of numbers")],
            execute=self._avg,
        ))

        self.register(Operation(
            identifier="First",
            friendly_name="First",
            description="Returns the first element of a collection",
            category="Collections/Access",
            required_args=[ArgInfo("collection", "The collection")],
            execute=self._first,
        ))

        self.register(Operation(
            identifier="Last",
            friendly_name="Last",
            description="Returns the last element of a collection",
            category="Collections/Access",
            required_args=[ArgInfo("collection", "The collection")],
            execute=self._last,
        ))

        self.register(Operation(
            identifier="Take",
            friendly_name="Take",
            description="Returns the first n elements of a collection",
            category="Collections/Slice",
            required_args=[
                ArgInfo("collection", "The collection"),
                ArgInfo("n", "Number of elements to take"),
            ],
            execute=self._take,
        ))

        self.register(Operation(
            identifier="Skip",
            friendly_name="Skip",
            description="Skips the first n elements and returns the rest",
            category="Collections/Slice",
            required_args=[
                ArgInfo("collection", "The collection"),
                ArgInfo("n", "Number of elements to skip"),
            ],
            execute=self._skip,
        ))

    def _list(self, args: list["MathObject"], session: "Session") -> "MathObject":
        return List(args)

    def _range(self, args: list["MathObject"], session: "Session") -> "MathObject":
        start = args[0]
        end = args[1]
        step = args[2] if len(args) > 2 else Scalar(1)

        if not all(isinstance(a, Scalar) for a in [start, end, step]):
            raise TypeError("Range requires numeric arguments")

        start_val = start.value
        end_val = end.value
        step_val = step.value

        if step_val == 0:
            raise ArgumentError("Range step cannot be zero")

        # Return a lazy Interval instead of eagerly creating a List
        return Interval(start_val, end_val, step_val)

    def _length(self, args: list["MathObject"], session: "Session") -> "MathObject":
        collection = args[0]
        if _is_collection(collection):
            return Scalar(len(collection))
        if isinstance(collection, Scalar) and isinstance(collection.value, str):
            return Scalar(len(collection.value))
        raise TypeError(f"Length expects a collection or string, got {collection.type_name}")

    def _map(self, args: list["MathObject"], session: "Session") -> "MathObject":
        from mathlang.engine.evaluator import evaluate_expression

        coll, func = args[0], args[1]
        if not _is_collection(coll):
            raise TypeError(f"Map expects a collection, got {coll.type_name}")
        if not isinstance(func, Lambda):
            raise TypeError(f"Map expects a lambda, got {func.type_name}")
        if func.arity != 1:
            raise ArgumentError(f"Map function must take 1 argument, got {func.arity}")

        result = []
        for item in coll:  # Works with any iterable
            child = session.create_child()
            child.set(func.parameters[0], item)
            result.append(evaluate_expression(func.body, child))

        return List(result)

    def _filter(self, args: list["MathObject"], session: "Session") -> "MathObject":
        from mathlang.engine.evaluator import evaluate_expression
        from mathlang.types.coercion import is_truthy

        coll, pred = args[0], args[1]
        if not _is_collection(coll):
            raise TypeError(f"Filter expects a collection, got {coll.type_name}")
        if not isinstance(pred, Lambda):
            raise TypeError(f"Filter expects a lambda, got {pred.type_name}")
        if pred.arity != 1:
            raise ArgumentError(f"Filter predicate must take 1 argument, got {pred.arity}")

        result = []
        for item in coll:  # Works with any iterable
            child = session.create_child()
            child.set(pred.parameters[0], item)
            if is_truthy(evaluate_expression(pred.body, child)):
                result.append(item)

        return List(result)

    def _reduce(self, args: list["MathObject"], session: "Session") -> "MathObject":
        from mathlang.engine.evaluator import evaluate_expression

        coll, func, initial = args[0], args[1], args[2]
        if not _is_collection(coll):
            raise TypeError(f"Reduce expects a collection, got {coll.type_name}")
        if not isinstance(func, Lambda):
            raise TypeError(f"Reduce expects a lambda, got {func.type_name}")
        if func.arity != 2:
            raise ArgumentError(f"Reduce function must take 2 arguments, got {func.arity}")

        acc = initial
        for item in coll:  # Works with any iterable
            child = session.create_child()
            child.set(func.parameters[0], acc)
            child.set(func.parameters[1], item)
            acc = evaluate_expression(func.body, child)

        return acc

    def _sum(self, args: list["MathObject"], session: "Session") -> "MathObject":
        coll = args[0]
        if not _is_collection(coll):
            raise TypeError(f"Sum expects a collection, got {coll.type_name}")

        total = 0
        for item in coll:  # Works with any iterable
            if not isinstance(item, Scalar):
                raise TypeError(f"Sum expects numeric elements, got {item.type_name}")
            total += item.value

        return Scalar(total)

    def _avg(self, args: list["MathObject"], session: "Session") -> "MathObject":
        coll = args[0]
        if not _is_collection(coll):
            raise TypeError(f"Avg expects a collection, got {coll.type_name}")
        if len(coll) == 0:
            raise ArgumentError("Cannot compute average of empty collection")

        total = 0
        count = 0
        for item in coll:  # Works with any iterable
            if not isinstance(item, Scalar):
                raise TypeError(f"Avg expects numeric elements, got {item.type_name}")
            total += item.value
            count += 1

        return Scalar(total / count)

    def _first(self, args: list["MathObject"], session: "Session") -> "MathObject":
        coll = args[0]
        if not _is_collection(coll):
            raise TypeError(f"First expects a collection, got {coll.type_name}")
        if len(coll) == 0:
            raise ArgumentError("Cannot get first element of empty collection")
        return coll[0]

    def _last(self, args: list["MathObject"], session: "Session") -> "MathObject":
        coll = args[0]
        if not _is_collection(coll):
            raise TypeError(f"Last expects a collection, got {coll.type_name}")
        if len(coll) == 0:
            raise ArgumentError("Cannot get last element of empty collection")
        return coll[-1]

    def _take(self, args: list["MathObject"], session: "Session") -> "MathObject":
        coll, n = args[0], args[1]
        if not _is_collection(coll):
            raise TypeError(f"Take expects a collection, got {coll.type_name}")
        if not isinstance(n, Scalar) or not isinstance(n.value, int):
            raise TypeError(f"Take count must be an integer, got {n.type_name}")

        count = n.value
        if count <= 0:
            return List([])

        # For List, use direct slicing
        if isinstance(coll, List):
            return List(coll.items[:count])

        # For Interval, use indexing (O(1) per element, no materialization)
        result = []
        for i in range(min(count, len(coll))):
            result.append(coll[i])
        return List(result)

    def _skip(self, args: list["MathObject"], session: "Session") -> "MathObject":
        coll, n = args[0], args[1]
        if not _is_collection(coll):
            raise TypeError(f"Skip expects a collection, got {coll.type_name}")
        if not isinstance(n, Scalar) or not isinstance(n.value, int):
            raise TypeError(f"Skip count must be an integer, got {n.type_name}")

        skip_count = n.value
        if skip_count <= 0:
            # Return all elements
            if isinstance(coll, List):
                return List(coll.items[:])
            # For Interval, must iterate but don't materialize upfront
            return List([item for item in coll])

        # For List, use direct slicing
        if isinstance(coll, List):
            return List(coll.items[skip_count:])

        # For Interval, use indexing (O(1) per element)
        total = len(coll)
        if skip_count >= total:
            return List([])
        result = []
        for i in range(skip_count, total):
            result.append(coll[i])
        return List(result)
