"""Tests for the AST module."""

import pytest
from mathlang.lang.ast import (
    NumberLiteral,
    StringLiteral,
    Identifier,
    NamedConstant,
    ArrayIndex,
    UnaryOp,
    BinaryOp,
    FunctionCall,
    LambdaExpr,
    Assignment,
    ExpressionStatement,
    Program,
    expr_to_string,
)


class TestExprToStringNumbers:
    """Tests for expr_to_string with number literals."""

    def test_integer(self):
        expr = NumberLiteral(42)
        assert expr_to_string(expr) == "42"

    def test_float(self):
        expr = NumberLiteral(3.14)
        assert expr_to_string(expr) == "3.14"

    def test_complex_pure_imaginary(self):
        expr = NumberLiteral(5j)
        assert expr_to_string(expr) == "5.0i"

    def test_complex_with_real(self):
        expr = NumberLiteral(3 + 4j)
        result = expr_to_string(expr)
        assert "3.0" in result
        assert "4.0i" in result


class TestExprToStringBasic:
    """Tests for expr_to_string with basic expressions."""

    def test_string_literal(self):
        expr = StringLiteral("hello")
        assert expr_to_string(expr) == '"hello"'

    def test_identifier(self):
        expr = Identifier("x")
        assert expr_to_string(expr) == "x"

    def test_named_constant(self):
        expr = NamedConstant("PI")
        assert expr_to_string(expr) == "[[PI]]"


class TestExprToStringOperators:
    """Tests for expr_to_string with operators."""

    def test_unary_op(self):
        expr = UnaryOp("-", NumberLiteral(5))
        assert expr_to_string(expr) == "-5"

    def test_binary_op(self):
        expr = BinaryOp("+", NumberLiteral(1), NumberLiteral(2))
        assert expr_to_string(expr) == "1 + 2"

    def test_nested_binary_ops(self):
        inner_left = BinaryOp("+", NumberLiteral(1), NumberLiteral(2))
        inner_right = BinaryOp("*", NumberLiteral(3), NumberLiteral(4))
        expr = BinaryOp("-", inner_left, inner_right)
        result = expr_to_string(expr)
        assert "(1 + 2)" in result
        assert "(3 * 4)" in result


class TestExprToStringArrayIndex:
    """Tests for expr_to_string with array indexing."""

    def test_array_index(self):
        expr = ArrayIndex(Identifier("arr"), NumberLiteral(0))
        assert expr_to_string(expr) == "arr[0]"

    def test_nested_array_index(self):
        expr = ArrayIndex(
            ArrayIndex(Identifier("matrix"), NumberLiteral(0)),
            NumberLiteral(1),
        )
        assert expr_to_string(expr) == "matrix[0][1]"


class TestExprToStringFunctionCall:
    """Tests for expr_to_string with function calls."""

    def test_no_args(self):
        expr = FunctionCall("Now", [])
        assert expr_to_string(expr) == "Now()"

    def test_one_arg(self):
        expr = FunctionCall("Sin", [Identifier("x")])
        assert expr_to_string(expr) == "Sin(x)"

    def test_multiple_args(self):
        expr = FunctionCall("Max", [NumberLiteral(1), NumberLiteral(2), NumberLiteral(3)])
        assert expr_to_string(expr) == "Max(1, 2, 3)"


class TestExprToStringLambda:
    """Tests for expr_to_string with lambda expressions."""

    def test_no_params(self):
        expr = LambdaExpr([], NumberLiteral(42))
        assert expr_to_string(expr) == "() -> 42"

    def test_single_param(self):
        expr = LambdaExpr(["x"], BinaryOp("^", Identifier("x"), NumberLiteral(2)))
        result = expr_to_string(expr)
        assert result == "x -> x ^ 2"

    def test_multi_params(self):
        expr = LambdaExpr(
            ["x", "y"], BinaryOp("+", Identifier("x"), Identifier("y"))
        )
        result = expr_to_string(expr)
        assert "(x, y)" in result
        assert "x + y" in result


class TestExprToStringUnknown:
    """Tests for expr_to_string with unknown expressions."""

    def test_unknown_expression(self):
        # Create a mock object that doesn't match any pattern
        class UnknownExpr:
            pass

        result = expr_to_string(UnknownExpr())  # type: ignore
        assert result == "<expr>"


class TestASTNodes:
    """Tests for AST node creation."""

    def test_assignment(self):
        stmt = Assignment("x", NumberLiteral(10))
        assert stmt.name == "x"
        assert isinstance(stmt.value, NumberLiteral)

    def test_expression_statement(self):
        stmt = ExpressionStatement(NumberLiteral(42))
        assert isinstance(stmt.expression, NumberLiteral)

    def test_program(self):
        stmts = [
            Assignment("x", NumberLiteral(10)),
            ExpressionStatement(Identifier("x")),
        ]
        prog = Program(stmts)
        assert len(prog.statements) == 2
