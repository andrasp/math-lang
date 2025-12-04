"""AST evaluator - transforms AST nodes into values."""

from typing import Sequence

from mathlang.lang import ast
from mathlang.lang.parser import parse
from mathlang.types.base import MathObject
from mathlang.types.scalar import Scalar
from mathlang.types.callable import Lambda, Thunk
from mathlang.types.coercion import coerce_numeric
from mathlang.engine.session import Session
from mathlang.engine.errors import (
    UndefinedVariableError,
    UndefinedOperationError,
    DivisionByZeroError,
    TypeError,
)
from mathlang.operations.registry import get_operation


class EvaluationResult:
    """Result of evaluating a statement."""

    def __init__(
        self,
        value: MathObject | None,
        is_assignment: bool = False,
        variable_name: str | None = None,
    ):
        self.value = value
        self.is_assignment = is_assignment
        self.variable_name = variable_name


def evaluate(source: str, session: Session | None = None) -> list[EvaluationResult]:
    """
    Parse and evaluate source code, returning results for each statement.

    Args:
        source: The source code to evaluate
        session: Optional session for variable persistence. Creates new if None.

    Returns:
        List of EvaluationResult for each statement
    """
    if session is None:
        session = Session()

    program = parse(source)
    return evaluate_program(program, session)


def evaluate_program(program: ast.Program, session: Session) -> list[EvaluationResult]:
    """Evaluate a parsed program."""
    results = []
    for statement in program.statements:
        result = evaluate_statement(statement, session)
        results.append(result)
    return results


def evaluate_statement(stmt: ast.Statement, session: Session) -> EvaluationResult:
    """Evaluate a single statement."""
    if isinstance(stmt, ast.Assignment):
        value = evaluate_expression(stmt.value, session)
        session.set(stmt.name, value)
        return EvaluationResult(value, is_assignment=True, variable_name=stmt.name)

    elif isinstance(stmt, ast.ExpressionStatement):
        value = evaluate_expression(stmt.expression, session)
        return EvaluationResult(value)

    raise TypeError(f"Unknown statement type: {type(stmt)}")


def evaluate_expression(expr: ast.Expression, session: Session) -> MathObject:
    """Evaluate an expression node."""

    if isinstance(expr, ast.NumberLiteral):
        return Scalar(expr.value)

    elif isinstance(expr, ast.StringLiteral):
        return Scalar(expr.value)

    elif isinstance(expr, ast.Identifier):
        value = session.get(expr.name)
        if value is None:
            raise UndefinedVariableError(expr.name)
        return value

    elif isinstance(expr, ast.NamedConstant):
        # Named constants are looked up as operations (from ConstantsProvider)
        operation = get_operation(expr.name)
        if operation is None:
            raise UndefinedVariableError(f"[[{expr.name}]]")
        return operation.execute([], session)

    elif isinstance(expr, ast.UnaryOp):
        operand = evaluate_expression(expr.operand, session)
        return evaluate_unary(expr.operator, operand)

    elif isinstance(expr, ast.BinaryOp):
        left = evaluate_expression(expr.left, session)
        right = evaluate_expression(expr.right, session)
        return evaluate_binary(expr.operator, left, right)

    elif isinstance(expr, ast.FunctionCall):
        return evaluate_function_call(expr, session)

    elif isinstance(expr, ast.ArrayIndex):
        array = evaluate_expression(expr.array, session)
        index = evaluate_expression(expr.index, session)
        return evaluate_array_index(array, index)

    elif isinstance(expr, ast.LambdaExpr):
        return Lambda(expr.parameters, expr.body)

    raise TypeError(f"Unknown expression type: {type(expr)}")


def evaluate_unary(operator: str, operand: MathObject) -> MathObject:
    """Evaluate a unary operation."""
    if operator == "-":
        if isinstance(operand, Scalar):
            return -operand
        raise TypeError(f"Cannot negate {operand.type_name}")

    raise UndefinedOperationError(operator)


def evaluate_binary(operator: str, left: MathObject, right: MathObject) -> MathObject:
    """Evaluate a binary operation."""
    # Try built-in operators first
    if isinstance(left, Scalar) and isinstance(right, Scalar):
        left_val, right_val = coerce_numeric(left, right)

        if operator == "+":
            return Scalar(left_val + right_val)
        elif operator == "-":
            return Scalar(left_val - right_val)
        elif operator == "*":
            return Scalar(left_val * right_val)
        elif operator == "/":
            if right_val == 0:
                raise DivisionByZeroError()
            return Scalar(left_val / right_val)
        elif operator == "%":
            if right_val == 0:
                raise DivisionByZeroError()
            return Scalar(left_val % right_val)
        elif operator == "^":
            return Scalar(left_val ** right_val)
        elif operator == ">":
            return Scalar(left_val > right_val)
        elif operator == ">=":
            return Scalar(left_val >= right_val)
        elif operator == "<":
            return Scalar(left_val < right_val)
        elif operator == "<=":
            return Scalar(left_val <= right_val)
        elif operator == "==":
            return Scalar(left_val == right_val)
        elif operator == "!=":
            return Scalar(left_val != right_val)

    # Fall back to operation registry for custom operators
    operation = get_operation(operator)
    if operation is not None:
        return operation.execute([left, right], Session())

    raise TypeError(f"Cannot apply '{operator}' to {left.type_name} and {right.type_name}")


def evaluate_function_call(call: ast.FunctionCall, session: Session) -> MathObject:
    """Evaluate a function call."""
    # Check if it's a variable holding a lambda
    var = session.get(call.name)
    if var is not None and isinstance(var, Lambda):
        return invoke_lambda(var, call.arguments, session)

    # Look up in operation registry
    operation = get_operation(call.name)
    if operation is None:
        raise UndefinedOperationError(call.name)

    # Evaluate arguments (but keep lambdas as Lambda objects, and defer lazy args)
    args: list[MathObject] = []
    for i, arg in enumerate(call.arguments):
        if isinstance(arg, ast.LambdaExpr):
            args.append(Lambda(arg.parameters, arg.body))
        elif i in operation.lazy_arg_indices:
            # Wrap in Thunk for lazy evaluation
            args.append(Thunk(arg, session))
        else:
            args.append(evaluate_expression(arg, session))

    return operation.execute(args, session)


def invoke_lambda(
    lam: Lambda,
    arguments: Sequence[ast.Expression | ast.LambdaExpr],
    session: Session,
) -> MathObject:
    """Invoke a lambda with the given arguments."""
    if len(arguments) != lam.arity:
        raise TypeError(f"Lambda expects {lam.arity} arguments, got {len(arguments)}")

    # Create child session with parameters bound
    child_session = session.create_child()
    for param, arg in zip(lam.parameters, arguments):
        if isinstance(arg, ast.LambdaExpr):
            child_session.set(param, Lambda(arg.parameters, arg.body))
        else:
            child_session.set(param, evaluate_expression(arg, session))

    # Evaluate lambda body in child session
    return evaluate_expression(lam.body, child_session)


def evaluate_array_index(array: MathObject, index: MathObject) -> MathObject:
    """Evaluate array indexing."""
    from mathlang.types.vector import Vector
    from mathlang.types.collection import List

    if not isinstance(index, Scalar) or not isinstance(index.value, int):
        raise TypeError(f"Array index must be an integer, got {index.type_name}")

    idx = index.value

    if isinstance(array, Vector):
        if idx < 0 or idx >= len(array):
            raise TypeError(f"Index {idx} out of bounds for vector of length {len(array)}")
        return array[idx]

    elif isinstance(array, List):
        if idx < 0 or idx >= len(array):
            raise TypeError(f"Index {idx} out of bounds for list of length {len(array)}")
        return array[idx]

    raise TypeError(f"Cannot index into {array.type_name}")
