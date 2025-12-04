"""Main CLI entry point."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from cli.runner import run_file
from cli.repl import start_repl
from cli.formatters import format_result, format_error

app = typer.Typer(
    name="mlang",
    help="MathLang - A mathematical expression language",
    no_args_is_help=True,
)
console = Console()


@app.command()
def eval(
    expression: str = typer.Argument(..., help="Expression to evaluate"),
) -> None:
    """Evaluate a single expression."""
    from mathlang.engine import Session, evaluate

    session = Session()
    try:
        results = evaluate(expression, session)
        for result in results:
            if result.value is not None:
                console.print(format_result(result))
    except Exception as e:
        console.print(format_error(e))
        raise typer.Exit(1)


@app.command()
def run(
    script: Path = typer.Argument(..., help="Path to .mlang script file"),
    var: Optional[list[str]] = typer.Option(
        None,
        "--var",
        "-v",
        help="Set a variable (format: name=value)",
    ),
) -> None:
    """Run a MathLang script file."""
    if not script.exists():
        console.print(f"[red]Error:[/red] File not found: {script}")
        raise typer.Exit(1)

    if not script.suffix == ".mlang":
        console.print(f"[yellow]Warning:[/yellow] Expected .mlang extension, got {script.suffix}")

    # Parse variable arguments
    variables: dict[str, str] = {}
    if var:
        for v in var:
            if "=" not in v:
                console.print(f"[red]Error:[/red] Invalid variable format: {v} (expected name=value)")
                raise typer.Exit(1)
            name, value = v.split("=", 1)
            variables[name] = value

    try:
        results = run_file(script, variables)
        for result in results:
            if result.value is not None and not result.is_assignment:
                console.print(format_result(result))
    except Exception as e:
        console.print(format_error(e))
        raise typer.Exit(1)


@app.command()
def repl() -> None:
    """Start an interactive REPL session."""
    start_repl()


@app.command()
def ops() -> None:
    """List all available operations."""
    from mathlang.operations.registry import list_operations_by_category

    categories = list_operations_by_category()

    for category, operations in sorted(categories.items()):
        console.print(f"\n[bold cyan]{category}[/bold cyan]")
        table = Table(show_header=True, header_style="bold")
        table.add_column("Name", style="green")
        table.add_column("Description")

        for op in sorted(operations, key=lambda o: o.identifier):
            table.add_row(op.identifier, op.description)

        console.print(table)


@app.command()
def version() -> None:
    """Show version information."""
    from mathlang import __version__
    console.print(f"MathLang v{__version__}")


if __name__ == "__main__":
    app()
