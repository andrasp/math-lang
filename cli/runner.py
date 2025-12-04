"""Script file execution."""

from pathlib import Path

from mathlang.engine import Session, evaluate
from mathlang.engine.evaluator import EvaluationResult
from mathlang.types.scalar import Scalar


def run_file(
    script_path: Path,
    variables: dict[str, str] | None = None,
) -> list[EvaluationResult]:
    """
    Run a MathLang script file.

    Args:
        script_path: Path to the .mlang file
        variables: Optional dict of variable name -> value strings

    Returns:
        List of evaluation results
    """
    session = Session()

    # Pre-populate variables from command line
    if variables:
        for name, value_str in variables.items():
            # Try to parse as number, fall back to string
            try:
                if "." in value_str:
                    value = float(value_str)
                else:
                    value = int(value_str)
                session.set(name, Scalar(value))
            except ValueError:
                session.set(name, Scalar(value_str))

    source = script_path.read_text()
    return evaluate(source, session)
