"""Parser that converts source text to AST using Lark."""

from pathlib import Path

from lark import Lark, Transformer, v_args, Token

from mathlang.lang import ast


_GRAMMAR_PATH = Path(__file__).parent / "grammar.lark"


@v_args(inline=True)
class ASTTransformer(Transformer):
    """Transforms Lark parse tree into our AST nodes."""

    def program(self, *statements):
        return ast.Program([s for s in statements if s is not None])

    def assignment(self, name, value):
        return ast.Assignment(str(name), value)

    def expression_stmt(self, expr):
        return ast.ExpressionStatement(expr)

    def single_param_lambda(self, param, _arrow, body):
        return ast.LambdaExpr([str(param)], body)

    def no_param_lambda(self, _empty, _arrow, body):
        return ast.LambdaExpr([], body)

    def multi_param_lambda(self, params, _arrow, body):
        return ast.LambdaExpr(params, body)

    def param_list(self, *params):
        return [str(p) for p in params]

    def no_param_func_def(self, name, _empty_parens, body):
        return ast.Assignment(str(name), ast.LambdaExpr([], body))

    def single_param_func_def(self, name, param, body):
        return ast.Assignment(str(name), ast.LambdaExpr([str(param)], body))

    def multi_param_func_def(self, name, params, body):
        return ast.Assignment(str(name), ast.LambdaExpr(params, body))

    def func_def_params(self, *params):
        return [str(p) for p in params]

    def binary_op(self, left, op, right):
        return ast.BinaryOp(str(op), left, right)

    def unary_op(self, op, operand):
        return ast.UnaryOp(str(op), operand)

    def func_call(self, name, *args):
        arguments = []
        for arg in args:
            if isinstance(arg, list):
                arguments.extend(arg)
            elif arg is not None:
                arguments.append(arg)
        return ast.FunctionCall(str(name), arguments)

    def no_arg_func_call(self, name, _empty_parens):
        return ast.FunctionCall(str(name), [])

    def func_args(self, *args):
        return list(args)

    def func_arg(self, arg):
        return arg

    def array_index(self, name, index):
        return ast.ArrayIndex(ast.Identifier(str(name)), index)

    def named_constant(self, name):
        return ast.NamedConstant(str(name))

    def identifier(self, name):
        return ast.Identifier(str(name))

    def number(self, token):
        text = str(token).rstrip("uUlLfFdDmM")
        if "." in text or "e" in text.lower():
            return ast.NumberLiteral(float(text))
        elif text.startswith("0x") or text.startswith("0X"):
            return ast.NumberLiteral(int(text, 16))
        else:
            return ast.NumberLiteral(int(text))

    def string(self, token):
        return ast.StringLiteral(str(token)[1:-1])

    def complex_number(self, token):
        text = str(token).lower().replace("i", "j").replace(" ", "")
        return ast.NumberLiteral(complex(text))


def _create_parser() -> Lark:
    """Create and return the Lark parser."""
    grammar = _GRAMMAR_PATH.read_text()
    return Lark(
        grammar,
        start="program",
        parser="earley",  # Earley parser handles ambiguous grammars
        ambiguity="resolve",  # Choose first match based on priority
    )


_parser: Lark | None = None
_transformer = ASTTransformer()


def parse(source: str) -> ast.Program:
    """Parse source code and return the AST."""
    global _parser
    if _parser is None:
        _parser = _create_parser()
    tree = _parser.parse(source)
    return _transformer.transform(tree)
