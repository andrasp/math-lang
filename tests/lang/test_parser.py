"""Tests for the parser."""

import pytest

from mathlang.lang.parser import parse
from mathlang.lang import ast


class TestBasicParsing:
    """Test basic expression parsing."""

    def test_number_literal(self):
        result = parse("42")
        assert len(result.statements) == 1
        stmt = result.statements[0]
        assert isinstance(stmt, ast.ExpressionStatement)
        assert isinstance(stmt.expression, ast.NumberLiteral)
        assert stmt.expression.value == 42

    def test_float_literal(self):
        result = parse("3.14")
        stmt = result.statements[0]
        assert isinstance(stmt, ast.ExpressionStatement)
        assert isinstance(stmt.expression, ast.NumberLiteral)
        assert stmt.expression.value == 3.14

    def test_string_literal(self):
        result = parse('"hello"')
        stmt = result.statements[0]
        assert isinstance(stmt, ast.ExpressionStatement)
        assert isinstance(stmt.expression, ast.StringLiteral)
        assert stmt.expression.value == "hello"

    def test_identifier(self):
        result = parse("x")
        stmt = result.statements[0]
        assert isinstance(stmt, ast.ExpressionStatement)
        assert isinstance(stmt.expression, ast.Identifier)
        assert stmt.expression.name == "x"


class TestOperators:
    """Test operator parsing."""

    def test_binary_add(self):
        result = parse("1 + 2")
        stmt = result.statements[0]
        assert isinstance(stmt, ast.ExpressionStatement)
        expr = stmt.expression
        assert isinstance(expr, ast.BinaryOp)
        assert expr.operator == "+"

    def test_binary_precedence(self):
        result = parse("1 + 2 * 3")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.BinaryOp)
        assert expr.operator == "+"
        # Right side should be 2 * 3
        assert isinstance(expr.right, ast.BinaryOp)
        assert expr.right.operator == "*"

    def test_unary_negation(self):
        result = parse("-5")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.UnaryOp)
        assert expr.operator == "-"

    def test_power_right_associative(self):
        result = parse("2 ^ 3 ^ 4")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.BinaryOp)
        assert expr.operator == "^"
        # Should be 2 ^ (3 ^ 4), so right side is binary
        assert isinstance(expr.right, ast.BinaryOp)


class TestAssignment:
    """Test assignment parsing."""

    def test_simple_assignment(self):
        result = parse("x = 10")
        stmt = result.statements[0]
        assert isinstance(stmt, ast.Assignment)
        assert stmt.name == "x"
        assert isinstance(stmt.value, ast.NumberLiteral)

    def test_expression_assignment(self):
        result = parse("y = 1 + 2")
        stmt = result.statements[0]
        assert isinstance(stmt, ast.Assignment)
        assert stmt.name == "y"
        assert isinstance(stmt.value, ast.BinaryOp)


class TestFunctionCalls:
    """Test function call parsing."""

    def test_no_args(self):
        result = parse("Foo()")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.FunctionCall)
        assert expr.name == "Foo"
        assert len(expr.arguments) == 0

    def test_one_arg(self):
        result = parse("Sin(x)")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.FunctionCall)
        assert expr.name == "Sin"
        assert len(expr.arguments) == 1

    def test_multiple_args(self):
        result = parse("Max(1, 2, 3)")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.FunctionCall)
        assert expr.name == "Max"
        assert len(expr.arguments) == 3


class TestLambda:
    """Test lambda expression parsing."""

    def test_single_param_lambda(self):
        result = parse("x -> x + 1")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.LambdaExpr)
        assert expr.parameters == ["x"]

    def test_multi_param_lambda(self):
        result = parse("(x, y) -> x + y")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.LambdaExpr)
        assert expr.parameters == ["x", "y"]

    def test_no_param_lambda(self):
        result = parse("() -> 42")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.LambdaExpr)
        assert expr.parameters == []


class TestNamedConstants:
    """Test named constant parsing."""

    def test_named_constant(self):
        result = parse("[[PI]]")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.NamedConstant)
        assert expr.name == "PI"


class TestMultipleStatements:
    """Test parsing multiple statements."""

    def test_semicolon_separated(self):
        result = parse("x = 1; y = 2")
        assert len(result.statements) == 2

    def test_newline_separated(self):
        result = parse("x = 1\ny = 2")
        assert len(result.statements) == 2


class TestFunctionDefinitions:
    """Test function definition syntax (f(x) = expr)."""

    def test_single_param_func_def(self):
        result = parse("square(x) = x^2")
        stmt = result.statements[0]
        assert isinstance(stmt, ast.Assignment)
        assert stmt.name == "square"
        assert isinstance(stmt.value, ast.LambdaExpr)
        assert stmt.value.parameters == ["x"]

    def test_multi_param_func_def(self):
        result = parse("add(a, b) = a + b")
        stmt = result.statements[0]
        assert isinstance(stmt, ast.Assignment)
        assert stmt.name == "add"
        assert isinstance(stmt.value, ast.LambdaExpr)
        assert stmt.value.parameters == ["a", "b"]

    def test_no_param_func_def(self):
        result = parse("getPI() = [[PI]]")
        stmt = result.statements[0]
        assert isinstance(stmt, ast.Assignment)
        assert stmt.name == "getPI"
        assert isinstance(stmt.value, ast.LambdaExpr)
        assert stmt.value.parameters == []


class TestArrayIndex:
    """Test array indexing syntax."""

    def test_array_index(self):
        result = parse("data[0]")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.ArrayIndex)
        assert isinstance(expr.array, ast.Identifier)
        assert expr.array.name == "data"

    def test_array_index_expression(self):
        result = parse("data[i + 1]")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.ArrayIndex)
        assert isinstance(expr.index, ast.BinaryOp)


class TestComplexNumbers:
    """Test complex number parsing."""

    def test_imaginary_only(self):
        result = parse("2i")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.NumberLiteral)
        assert expr.value == 2j

    def test_complex_with_real(self):
        result = parse("3+2i")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.NumberLiteral)
        assert expr.value == 3 + 2j

    def test_complex_negative_imaginary(self):
        result = parse("3-2i")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.NumberLiteral)
        assert expr.value == 3 - 2j


class TestScientificNotation:
    """Test scientific notation parsing."""

    def test_scientific_notation(self):
        result = parse("1.5e10")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.NumberLiteral)
        assert expr.value == 1.5e10

    def test_scientific_notation_negative_exp(self):
        result = parse("1.5e-3")
        expr = result.statements[0].expression
        assert isinstance(expr, ast.NumberLiteral)
        assert expr.value == 0.0015


class TestComments:
    """Test comment handling."""

    def test_comment_ignored(self):
        result = parse("x = 1 # this is a comment")
        assert len(result.statements) == 1
        stmt = result.statements[0]
        assert isinstance(stmt, ast.Assignment)
        assert stmt.name == "x"

    def test_comment_line_ignored(self):
        result = parse("# full line comment\nx = 1")
        assert len(result.statements) == 1
