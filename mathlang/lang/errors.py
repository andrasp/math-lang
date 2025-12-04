"""Parse and syntax error definitions."""


class MathLangError(Exception):
    """Base exception for all MathLang errors."""
    pass


class ParseError(MathLangError):
    """Raised when parsing fails."""

    def __init__(self, message: str, line: int | None = None, column: int | None = None):
        self.line = line
        self.column = column
        location = ""
        if line is not None:
            location = f" at line {line}"
            if column is not None:
                location += f", column {column}"
        super().__init__(f"Parse error{location}: {message}")


class SyntaxError(ParseError):
    """Raised for syntax errors in the source."""
    pass
