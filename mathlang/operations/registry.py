"""Global operation registry."""

from mathlang.operations.base import Operation, OperationProvider

_providers: list[OperationProvider] = []
_operation_cache: dict[str, Operation] = {}


def register_provider(provider: OperationProvider) -> None:
    """Register an operation provider."""
    _providers.append(provider)
    for op in provider.list_operations():
        _operation_cache[op.identifier] = op


def get_operation(identifier: str) -> Operation | None:
    """Look up an operation by identifier."""
    return _operation_cache.get(identifier)


def list_operations() -> list[Operation]:
    """List all registered operations."""
    return list(_operation_cache.values())


def list_operations_by_category() -> dict[str, list[Operation]]:
    """List all operations grouped by category."""
    result: dict[str, list[Operation]] = {}
    for op in _operation_cache.values():
        if op.category not in result:
            result[op.category] = []
        result[op.category].append(op)
    return result


def _init_builtin_providers() -> None:
    """Initialize all built-in providers."""
    from mathlang.operations.providers.arithmetic import ArithmeticProvider
    from mathlang.operations.providers.trigonometry import TrigonometryProvider
    from mathlang.operations.providers.constants import ConstantsProvider
    from mathlang.operations.providers.logical import LogicalProvider
    from mathlang.operations.providers.lists import ListsProvider
    from mathlang.operations.providers.strings import StringsProvider
    from mathlang.operations.providers.statistics import StatisticsProvider
    from mathlang.operations.providers.combinatorics import CombinatoricsProvider
    from mathlang.operations.providers.vectors import VectorsProvider
    from mathlang.operations.providers.datetime import DateTimeProvider
    from mathlang.operations.providers.visualization import VisualizationProvider

    register_provider(ArithmeticProvider())
    register_provider(TrigonometryProvider())
    register_provider(ConstantsProvider())
    register_provider(LogicalProvider())
    register_provider(ListsProvider())
    register_provider(StringsProvider())
    register_provider(StatisticsProvider())
    register_provider(CombinatoricsProvider())
    register_provider(VectorsProvider())
    register_provider(DateTimeProvider())
    register_provider(VisualizationProvider())


_init_builtin_providers()
