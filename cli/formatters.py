"""Output formatting for CLI."""

from mathlang.engine.evaluator import EvaluationResult
from mathlang.types.result import Error


def format_result(result: EvaluationResult) -> str:
    """Format an evaluation result for display."""
    if result.value is None:
        return ""

    value = result.value

    if isinstance(value, Error):
        return f"[red]{value.display()}[/red]"

    display = value.display()
    type_name = value.type_name

    return f"{display} [dim]({type_name})[/dim]"


def format_error(error: Exception) -> str:
    """Format an error for display."""
    return f"[red]Error:[/red] {error}"
