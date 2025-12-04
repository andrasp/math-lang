"""AST node definitions for the math language."""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass


class Node(ABC):
    """Base class for all AST nodes."""
    pass


class Expression(Node):
    """Base class for expression nodes."""
    pass


class Statement(Node):
    """Base class for statement nodes."""
    pass


@dataclass
class NumberLiteral(Expression):
    """Numeric literal (int, float, or complex)."""
    value: int | float | complex


@dataclass
class StringLiteral(Expression):
    """String literal."""
    value: str


@dataclass
class Identifier(Expression):
    """Variable or function name reference."""
    name: str


@dataclass
class NamedConstant(Expression):
    """Named constant reference like [[PI]]."""
    name: str


@dataclass
class ArrayIndex(Expression):
    """Array indexing: arr[index]."""
    array: Expression
    index: Expression


@dataclass
class UnaryOp(Expression):
    """Unary operation: -x."""
    operator: str
    operand: Expression


@dataclass
class BinaryOp(Expression):
    """Binary operation: x + y."""
    operator: str
    left: Expression
    right: Expression


@dataclass
class FunctionCall(Expression):
    """Function call: Sin(x), Map(list, f)."""
    name: str
    arguments: list[Expression | "LambdaExpr"]


@dataclass
class LambdaExpr(Expression):
    """Lambda expression: x -> x^2, (x, y) -> x + y."""
    parameters: list[str]
    body: Expression


@dataclass
class Assignment(Statement):
    """Variable assignment: x = expr."""
    name: str
    value: Expression | LambdaExpr


@dataclass
class ExpressionStatement(Statement):
    """Standalone expression (printed to output)."""
    expression: Expression


@dataclass
class Program(Node):
    """Root node containing all statements."""
    statements: list[Statement]


def expr_to_string(expr: Expression) -> str:
    """Reconstruct a string representation from an AST expression."""
    match expr:
        case NumberLiteral(value=v):
            if isinstance(v, complex):
                if v.real == 0:
                    return f"{v.imag}i"
                return f"({v.real} + {v.imag}i)"
            return str(v)
        case StringLiteral(value=v):
            return f'"{v}"'
        case Identifier(name=n):
            return n
        case NamedConstant(name=n):
            return f"[[{n}]]"
        case ArrayIndex(array=arr, index=idx):
            return f"{expr_to_string(arr)}[{expr_to_string(idx)}]"
        case UnaryOp(operator=op, operand=operand):
            return f"{op}{expr_to_string(operand)}"
        case BinaryOp(operator=op, left=left, right=right):
            left_str = expr_to_string(left)
            right_str = expr_to_string(right)
            # Add parens for nested binary ops to preserve meaning
            if isinstance(left, BinaryOp):
                left_str = f"({left_str})"
            if isinstance(right, BinaryOp):
                right_str = f"({right_str})"
            return f"{left_str} {op} {right_str}"
        case FunctionCall(name=name, arguments=args):
            args_str = ", ".join(expr_to_string(a) for a in args)
            return f"{name}({args_str})"
        case LambdaExpr(parameters=params, body=body):
            body_str = expr_to_string(body)
            if not params:
                return f"() -> {body_str}"
            elif len(params) == 1:
                return f"{params[0]} -> {body_str}"
            else:
                return f"({', '.join(params)}) -> {body_str}"
        case _:
            return "<expr>"
