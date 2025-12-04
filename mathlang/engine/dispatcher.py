"""Operation dispatcher - routes calls to appropriate operations."""

# Note: Most dispatch logic is in evaluator.py and registry.py
# This module can be extended for more complex dispatch needs

from mathlang.operations.registry import get_operation, list_operations

__all__ = ["get_operation", "list_operations"]
