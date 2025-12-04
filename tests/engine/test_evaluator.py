"""Tests for the evaluator."""

import pytest
import math

from mathlang.engine import evaluate, Session
from mathlang.types.scalar import Scalar


class TestBasicEvaluation:
    """Test basic expression evaluation."""

    def test_number(self, session):
        results = evaluate("42", session)
        assert len(results) == 1
        assert results[0].value == Scalar(42)

    def test_float(self, session):
        results = evaluate("3.14", session)
        assert results[0].value.value == pytest.approx(3.14)

    def test_string(self, session):
        results = evaluate('"hello"', session)
        assert results[0].value == Scalar("hello")


class TestArithmetic:
    """Test arithmetic operations."""

    def test_addition(self, session):
        results = evaluate("1 + 2", session)
        assert results[0].value == Scalar(3)

    def test_subtraction(self, session):
        results = evaluate("5 - 3", session)
        assert results[0].value == Scalar(2)

    def test_multiplication(self, session):
        results = evaluate("3 * 4", session)
        assert results[0].value == Scalar(12)

    def test_division(self, session):
        results = evaluate("10 / 4", session)
        assert results[0].value.value == pytest.approx(2.5)

    def test_power(self, session):
        results = evaluate("2 ^ 3", session)
        assert results[0].value == Scalar(8)

    def test_modulo(self, session):
        results = evaluate("10 % 3", session)
        assert results[0].value == Scalar(1)

    def test_negation(self, session):
        results = evaluate("-5", session)
        assert results[0].value == Scalar(-5)

    def test_precedence(self, session):
        results = evaluate("1 + 2 * 3", session)
        assert results[0].value == Scalar(7)

    def test_parentheses(self, session):
        results = evaluate("(1 + 2) * 3", session)
        assert results[0].value == Scalar(9)


class TestComparison:
    """Test comparison operations."""

    def test_greater_than(self, session):
        results = evaluate("5 > 3", session)
        assert results[0].value == Scalar(True)

    def test_less_than(self, session):
        results = evaluate("3 < 5", session)
        assert results[0].value == Scalar(True)

    def test_equality(self, session):
        results = evaluate("5 == 5", session)
        assert results[0].value == Scalar(True)

    def test_inequality(self, session):
        results = evaluate("5 != 3", session)
        assert results[0].value == Scalar(True)


class TestVariables:
    """Test variable assignment and lookup."""

    def test_assignment(self, session):
        results = evaluate("x = 10", session)
        assert results[0].is_assignment
        assert results[0].variable_name == "x"
        assert session.get("x") == Scalar(10)

    def test_variable_lookup(self, session):
        evaluate("x = 5", session)
        results = evaluate("x + 3", session)
        assert results[0].value == Scalar(8)

    def test_undefined_variable(self, session):
        from mathlang.engine.errors import UndefinedVariableError

        with pytest.raises(UndefinedVariableError):
            evaluate("undefined_var", session)


class TestFunctions:
    """Test function calls."""

    def test_abs(self, session):
        results = evaluate("Abs(-5)", session)
        assert results[0].value == Scalar(5)

    def test_sqrt(self, session):
        results = evaluate("Sqrt(16)", session)
        assert results[0].value == Scalar(4.0)

    def test_sin(self, session):
        results = evaluate("Sin(0)", session)
        assert results[0].value.value == pytest.approx(0.0)

    def test_cos(self, session):
        results = evaluate("Cos(0)", session)
        assert results[0].value.value == pytest.approx(1.0)

    def test_max(self, session):
        results = evaluate("Max(1, 5, 3)", session)
        assert results[0].value == Scalar(5)

    def test_min(self, session):
        results = evaluate("Min(1, 5, 3)", session)
        assert results[0].value == Scalar(1)


class TestNamedConstants:
    """Test named constants."""

    def test_pi(self, session):
        results = evaluate("[[PI]]", session)
        assert results[0].value.value == pytest.approx(math.pi)

    def test_e(self, session):
        results = evaluate("[[E]]", session)
        assert results[0].value.value == pytest.approx(math.e)


class TestLists:
    """Test list operations."""

    def test_create_list(self, session):
        results = evaluate("List(1, 2, 3)", session)
        assert results[0].value.display() == "[1, 2, 3]"

    def test_sum(self, session):
        results = evaluate("Sum(List(1, 2, 3, 4))", session)
        assert results[0].value == Scalar(10)

    def test_length(self, session):
        results = evaluate("Length(List(1, 2, 3))", session)
        assert results[0].value == Scalar(3)


class TestLambdas:
    """Test lambda expressions."""

    def test_map_with_lambda(self, session):
        results = evaluate("Map(List(1, 2, 3), x -> x * 2)", session)
        result_list = results[0].value
        assert result_list.display() == "[2, 4, 6]"

    def test_filter_with_lambda(self, session):
        results = evaluate("Filter(List(1, 2, 3, 4), x -> x > 2)", session)
        result_list = results[0].value
        assert result_list.display() == "[3, 4]"

    def test_reduce_with_lambda(self, session):
        results = evaluate("Reduce(List(1, 2, 3, 4), (acc, x) -> acc + x, 0)", session)
        assert results[0].value == Scalar(10)


class TestUserDefinedFunctions:
    """Test user-defined function syntax and recursion."""

    def test_single_param_function(self, session):
        evaluate("square(x) = x^2", session)
        results = evaluate("square(5)", session)
        assert results[0].value == Scalar(25)

    def test_multi_param_function(self, session):
        evaluate("add(a, b) = a + b", session)
        results = evaluate("add(3, 4)", session)
        assert results[0].value == Scalar(7)

    def test_no_param_function(self, session):
        evaluate("getPI() = [[PI]]", session)
        results = evaluate("getPI()", session)
        assert results[0].value.value == pytest.approx(math.pi)

    def test_recursive_factorial(self, session):
        evaluate("factorial(n) = If(n <= 1, 1, n * factorial(n - 1))", session)
        results = evaluate("factorial(5)", session)
        assert results[0].value == Scalar(120)

    def test_recursive_fibonacci(self, session):
        evaluate("fib(n) = If(n <= 1, n, fib(n-1) + fib(n-2))", session)
        results = evaluate("fib(10)", session)
        assert results[0].value == Scalar(55)

    def test_function_composition(self, session):
        evaluate("double(x) = x * 2", session)
        evaluate("inc(x) = x + 1", session)
        results = evaluate("double(inc(5))", session)
        assert results[0].value == Scalar(12)


class TestLogicalOperations:
    """Test logical operations."""

    def test_and_true(self, session):
        results = evaluate("And(1, 2, 3)", session)
        assert results[0].value == Scalar(True)

    def test_and_false(self, session):
        results = evaluate("And(1, 0, 3)", session)
        assert results[0].value == Scalar(False)

    def test_or_true(self, session):
        results = evaluate("Or(0, 0, 1)", session)
        assert results[0].value == Scalar(True)

    def test_or_false(self, session):
        results = evaluate("Or(0, 0, 0)", session)
        assert results[0].value == Scalar(False)

    def test_not_true(self, session):
        results = evaluate("Not(0)", session)
        assert results[0].value == Scalar(True)

    def test_not_false(self, session):
        results = evaluate("Not(1)", session)
        assert results[0].value == Scalar(False)

    def test_if_true_branch(self, session):
        results = evaluate("If(1 > 0, 10, 20)", session)
        assert results[0].value == Scalar(10)

    def test_if_false_branch(self, session):
        results = evaluate("If(1 < 0, 10, 20)", session)
        assert results[0].value == Scalar(20)

    def test_is_nan_false(self, session):
        # Regular numbers are not NaN
        results = evaluate("IsNaN(5)", session)
        assert results[0].value == Scalar(False)

    def test_is_inf_false(self, session):
        # Regular numbers are not infinite
        results = evaluate("IsInf(5)", session)
        assert results[0].value == Scalar(False)


class TestStatisticsOperations:
    """Test statistics operations."""

    def test_mean(self, session):
        results = evaluate("Mean(List(1, 2, 3, 4, 5))", session)
        assert results[0].value.value == pytest.approx(3.0)

    def test_mean_with_interval(self, session):
        results = evaluate("Mean(Range(1, 11))", session)
        assert results[0].value.value == pytest.approx(5.5)

    def test_median_odd(self, session):
        results = evaluate("Median(List(1, 3, 5, 7, 9))", session)
        assert results[0].value == Scalar(5)

    def test_median_even(self, session):
        results = evaluate("Median(List(1, 2, 3, 4))", session)
        assert results[0].value.value == pytest.approx(2.5)

    def test_mode(self, session):
        results = evaluate("Mode(List(1, 2, 2, 3, 3, 3))", session)
        assert results[0].value == Scalar(3)

    def test_stddev(self, session):
        results = evaluate("StdDev(List(2, 4, 4, 4, 5, 5, 7, 9))", session)
        assert results[0].value.value == pytest.approx(2.138, rel=0.01)

    def test_variance(self, session):
        results = evaluate("Variance(List(2, 4, 4, 4, 5, 5, 7, 9))", session)
        assert results[0].value.value == pytest.approx(4.571, rel=0.01)

    def test_correlation(self, session):
        results = evaluate("Correlation(List(1, 2, 3, 4, 5), List(2, 4, 6, 8, 10))", session)
        assert results[0].value.value == pytest.approx(1.0)

    def test_percentile(self, session):
        results = evaluate("Percentile(List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), 50)", session)
        assert results[0].value.value == pytest.approx(5.5)

    def test_quartiles(self, session):
        results = evaluate("Quartiles(Range(1, 11))", session)
        assert results[0].value.display() == "[3.25, 5.5, 7.75]"

    def test_iqr(self, session):
        results = evaluate("IQR(Range(1, 11))", session)
        assert results[0].value.value == pytest.approx(4.5)


class TestStringOperations:
    """Test string operations."""

    def test_concat(self, session):
        results = evaluate('Concat("Hello", " ", "World")', session)
        assert results[0].value == Scalar("Hello World")

    def test_substring(self, session):
        results = evaluate('Substring("Hello World", 0, 5)', session)
        assert results[0].value == Scalar("Hello")

    def test_toupper(self, session):
        results = evaluate('ToUpper("hello")', session)
        assert results[0].value == Scalar("HELLO")

    def test_tolower(self, session):
        results = evaluate('ToLower("HELLO")', session)
        assert results[0].value == Scalar("hello")

    def test_trim(self, session):
        results = evaluate('Trim("  hello  ")', session)
        assert results[0].value == Scalar("hello")

    def test_replace(self, session):
        results = evaluate('Replace("hello world", "world", "there")', session)
        assert results[0].value == Scalar("hello there")

    def test_contains(self, session):
        results = evaluate('Contains("hello world", "world")', session)
        assert results[0].value == Scalar(True)

    def test_startswith(self, session):
        results = evaluate('StartsWith("hello world", "hello")', session)
        assert results[0].value == Scalar(True)

    def test_endswith(self, session):
        results = evaluate('EndsWith("hello world", "world")', session)
        assert results[0].value == Scalar(True)

    def test_split(self, session):
        results = evaluate('Split("a,b,c", ",")', session)
        assert results[0].value.display() == "[a, b, c]"

    def test_join(self, session):
        results = evaluate('Join(List("a", "b", "c"), "-")', session)
        assert results[0].value == Scalar("a-b-c")


class TestVectorOperations:
    """Test vector operations."""

    def test_vec_creation(self, session):
        results = evaluate("Vec(1, 2, 3)", session)
        assert results[0].value.display() == "[1, 2, 3]"

    def test_vec_from_list(self, session):
        results = evaluate("VecFromList(List(1, 2, 3))", session)
        assert results[0].value.display() == "[1, 2, 3]"

    def test_vec_from_interval(self, session):
        results = evaluate("VecFromList(Range(1, 4))", session)
        assert results[0].value.display() == "[1, 2, 3]"

    def test_dot_product(self, session):
        results = evaluate("DotProduct(Vec(1, 2, 3), Vec(4, 5, 6))", session)
        assert results[0].value == Scalar(32)

    def test_cross_product(self, session):
        results = evaluate("CrossProduct(Vec(1, 0, 0), Vec(0, 1, 0))", session)
        assert results[0].value.display() == "[0, 0, 1]"

    def test_magnitude(self, session):
        results = evaluate("Magnitude(Vec(3, 4))", session)
        assert results[0].value == Scalar(5.0)

    def test_normalize(self, session):
        results = evaluate("Magnitude(Normalize(Vec(3, 4)))", session)
        assert results[0].value.value == pytest.approx(1.0)

    def test_vec_add(self, session):
        results = evaluate("VecAdd(Vec(1, 2, 3), Vec(4, 5, 6))", session)
        assert results[0].value.display() == "[5, 7, 9]"

    def test_vec_sub(self, session):
        results = evaluate("VecSub(Vec(4, 5, 6), Vec(1, 2, 3))", session)
        assert results[0].value.display() == "[3, 3, 3]"

    def test_vec_scale(self, session):
        results = evaluate("VecScale(Vec(1, 2, 3), 2)", session)
        assert results[0].value.display() == "[2, 4, 6]"

    def test_vec_dim(self, session):
        results = evaluate("VecDim(Vec(1, 2, 3, 4, 5))", session)
        assert results[0].value == Scalar(5)


class TestCombinatoricsOperations:
    """Test combinatorics operations."""

    def test_factorial(self, session):
        results = evaluate("Factorial(5)", session)
        assert results[0].value == Scalar(120)

    def test_permutations(self, session):
        results = evaluate("Permutations(5, 3)", session)
        assert results[0].value == Scalar(60)

    def test_combinations(self, session):
        results = evaluate("Combinations(5, 3)", session)
        assert results[0].value == Scalar(10)

    def test_fibonacci(self, session):
        results = evaluate("Fibonacci(10)", session)
        assert results[0].value == Scalar(55)

    def test_gcd(self, session):
        results = evaluate("GCD(48, 18)", session)
        assert results[0].value == Scalar(6)

    def test_lcm(self, session):
        results = evaluate("LCM(4, 6)", session)
        assert results[0].value == Scalar(12)

    def test_is_prime(self, session):
        results = evaluate("IsPrime(17)", session)
        assert results[0].value == Scalar(True)

    def test_is_not_prime(self, session):
        results = evaluate("IsPrime(18)", session)
        assert results[0].value == Scalar(False)

    def test_prime_factors(self, session):
        results = evaluate("PrimeFactors(12)", session)
        assert results[0].value.display() == "[2, 2, 3]"


class TestCollectionsExtended:
    """Test collection operations with Range/Interval."""

    def test_range_basic(self, session):
        results = evaluate("Range(1, 5)", session)
        assert results[0].value.display() == "[1..5)"

    def test_range_with_step(self, session):
        results = evaluate("Range(0, 10, 2)", session)
        assert len(results[0].value) == 5

    def test_range_sum(self, session):
        results = evaluate("Sum(Range(1, 6))", session)
        assert results[0].value == Scalar(15)

    def test_range_map(self, session):
        results = evaluate("Map(Range(1, 4), x -> x * x)", session)
        assert results[0].value.display() == "[1, 4, 9]"

    def test_range_filter(self, session):
        results = evaluate("Filter(Range(1, 11), x -> x % 2 == 0)", session)
        assert results[0].value.display() == "[2, 4, 6, 8, 10]"

    def test_first(self, session):
        results = evaluate("First(Range(5, 10))", session)
        assert results[0].value == Scalar(5)

    def test_last(self, session):
        results = evaluate("Last(Range(5, 10))", session)
        assert results[0].value == Scalar(9)

    def test_take(self, session):
        results = evaluate("Take(Range(1, 100), 3)", session)
        assert results[0].value.display() == "[1, 2, 3]"

    def test_skip(self, session):
        results = evaluate("Skip(Range(1, 6), 2)", session)
        assert results[0].value.display() == "[3, 4, 5]"

    def test_array_index(self, session):
        evaluate("data = List(10, 20, 30, 40)", session)
        results = evaluate("data[2]", session)
        assert results[0].value == Scalar(30)

    def test_avg(self, session):
        results = evaluate("Avg(Range(1, 6))", session)
        assert results[0].value.value == pytest.approx(3.0)


class TestArithmeticExtended:
    """Test additional arithmetic operations."""

    def test_floor(self, session):
        results = evaluate("Floor(3.7)", session)
        assert results[0].value == Scalar(3)

    def test_ceiling(self, session):
        results = evaluate("Ceiling(3.2)", session)
        assert results[0].value == Scalar(4)

    def test_round(self, session):
        results = evaluate("Round(3.5)", session)
        assert results[0].value == Scalar(4)

    def test_log(self, session):
        results = evaluate("Log([[E]])", session)
        assert results[0].value.value == pytest.approx(1.0)

    def test_log10(self, session):
        results = evaluate("Log10(100)", session)
        assert results[0].value.value == pytest.approx(2.0)

    def test_exp(self, session):
        results = evaluate("Exp(1)", session)
        assert results[0].value.value == pytest.approx(math.e)


class TestTrigonometryExtended:
    """Test additional trigonometry operations."""

    def test_tan(self, session):
        results = evaluate("Tan(0)", session)
        assert results[0].value.value == pytest.approx(0.0)

    def test_arcsin(self, session):
        results = evaluate("ArcSin(1)", session)
        assert results[0].value.value == pytest.approx(math.pi / 2)

    def test_arccos(self, session):
        results = evaluate("ArcCos(1)", session)
        assert results[0].value.value == pytest.approx(0.0)

    def test_arctan(self, session):
        results = evaluate("ArcTan(1)", session)
        assert results[0].value.value == pytest.approx(math.pi / 4)

    def test_sinh(self, session):
        results = evaluate("Sinh(0)", session)
        assert results[0].value.value == pytest.approx(0.0)

    def test_cosh(self, session):
        results = evaluate("Cosh(0)", session)
        assert results[0].value.value == pytest.approx(1.0)

    def test_tanh(self, session):
        results = evaluate("Tanh(0)", session)
        assert results[0].value.value == pytest.approx(0.0)

    def test_atan2(self, session):
        results = evaluate("ArcTan2(1, 1)", session)
        assert results[0].value.value == pytest.approx(math.pi / 4)
