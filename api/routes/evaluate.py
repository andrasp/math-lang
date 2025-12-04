"""Evaluation endpoint."""

import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.sessions import session_manager

router = APIRouter()


class EvaluateRequest(BaseModel):
    """Request body for evaluation."""

    source: str
    session_id: str | None = None
    timeout_ms: int = 5000


class EvaluateResult(BaseModel):
    """Single evaluation result."""

    value: str
    type_name: str
    is_assignment: bool = False
    variable_name: str | None = None
    image_data: str | None = None  # Base64-encoded PNG for plot types


class ErrorDetail(BaseModel):
    """Error detail with location info."""

    message: str
    line: int | None = None
    column: int | None = None


class EvaluateResponse(BaseModel):
    """Response from evaluation."""

    session_id: str
    results: list[EvaluateResult]
    elapsed_ms: float
    variables: dict[str, dict[str, str]]
    error: ErrorDetail | None = None


@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_source(request: EvaluateRequest) -> EvaluateResponse:
    """Evaluate MathLang source code."""
    from mathlang.engine import evaluate
    from api.plotting import render_plot

    start_time = time.time()
    session_info = session_manager.get_or_create(request.session_id)

    try:
        results = evaluate(request.source, session_info.session)
        elapsed_ms = (time.time() - start_time) * 1000

        eval_results = []
        for r in results:
            # Check if result is a plot type and render it
            image_data = render_plot(r.value) if r.value else None
            eval_results.append(
                EvaluateResult(
                    value=r.value.display() if r.value else "",
                    type_name=r.value.type_name if r.value else "",
                    is_assignment=r.is_assignment,
                    variable_name=r.variable_name,
                    image_data=image_data,
                )
            )

        return EvaluateResponse(
            session_id=session_info.id,
            results=eval_results,
            elapsed_ms=elapsed_ms,
            variables=session_info.get_variables(),
        )
    except Exception as e:
        elapsed_ms = (time.time() - start_time) * 1000
        return EvaluateResponse(
            session_id=session_info.id,
            results=[],
            elapsed_ms=elapsed_ms,
            variables=session_info.get_variables(),
            error=ErrorDetail(message=str(e)),
        )
