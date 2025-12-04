"""Interactive REPL for MathLang."""

from rich.console import Console
from rich.prompt import Prompt

from mathlang.engine import Session, evaluate
from cli.formatters import format_result, format_error

console = Console()


def start_repl() -> None:
    """Start an interactive REPL session."""
    from mathlang import __version__

    console.print(f"[bold cyan]MathLang v{__version__}[/bold cyan]")
    console.print("Type expressions to evaluate. Type 'exit' or 'quit' to exit.")
    console.print("Type 'vars' to list variables, 'clear' to clear them.\n")

    session = Session()

    while True:
        try:
            line = Prompt.ask("[green]>>>[/green]", console=console)
        except (EOFError, KeyboardInterrupt):
            console.print("\nGoodbye!")
            break

        line = line.strip()

        if not line:
            continue

        if line.lower() in ("exit", "quit"):
            console.print("Goodbye!")
            break

        if line.lower() == "vars":
            variables = session.list_variables()
            if not variables:
                console.print("[dim]No variables defined[/dim]")
            else:
                for name, value in variables.items():
                    console.print(f"  [cyan]{name}[/cyan] = {value.display()} [dim]({value.type_name})[/dim]")
            continue

        if line.lower() == "clear":
            session.clear()
            console.print("[dim]Variables cleared[/dim]")
            continue

        if line.lower() == "ops":
            from mathlang.operations.registry import list_operations
            ops = list_operations()
            names = sorted(op.identifier for op in ops)
            console.print(", ".join(names))
            continue

        try:
            results = evaluate(line, session)
            for result in results:
                if result.is_assignment:
                    console.print(f"  [dim]{result.variable_name} = {result.value.display()}[/dim]")
                elif result.value is not None:
                    console.print(f"  {format_result(result)}")
        except Exception as e:
            console.print(format_error(e))
