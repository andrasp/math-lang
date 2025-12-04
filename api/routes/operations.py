"""Operations listing endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class OperationInfo(BaseModel):
    """Information about an operation."""

    identifier: str
    friendly_name: str
    description: str
    category: str


class OperationsResponse(BaseModel):
    """Response with list of operations."""

    operations: list[OperationInfo]


@router.get("/", response_model=OperationsResponse)
async def list_all_operations() -> OperationsResponse:
    """List all available operations."""
    from mathlang.operations.registry import list_operations

    ops = list_operations()
    return OperationsResponse(
        operations=[
            OperationInfo(
                identifier=op.identifier,
                friendly_name=op.friendly_name,
                description=op.description,
                category=op.category,
            )
            for op in sorted(ops, key=lambda o: (o.category, o.identifier))
        ]
    )


@router.get("/categories")
async def list_categories() -> dict[str, list[OperationInfo]]:
    """List operations grouped by category."""
    from mathlang.operations.registry import list_operations_by_category

    result = {}
    for category, ops in list_operations_by_category().items():
        result[category] = [
            OperationInfo(
                identifier=op.identifier,
                friendly_name=op.friendly_name,
                description=op.description,
                category=op.category,
            )
            for op in sorted(ops, key=lambda o: o.identifier)
        ]
    return result
