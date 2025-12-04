"""Additional coverage for ArithmeticProvider operations."""

import builtins
import math
import random

import pytest

from mathlang.engine.errors import ArgumentError
from mathlang.operations.providers.arithmetic import ArithmeticProvider
from mathlang.types.scalar import Scalar


@pytest.fixture
def provider() -> ArithmeticProvider:
    return ArithmeticProvider()

def test_name_and_registration(provider: ArithmeticProvider):
    assert provider.name == "Arithmetic"
    identifiers = {op.identifier for op in provider.list_operations()}
    for expected in {"Abs", "Sqrt", "Random"}:
        assert expected in identifiers


def test_sqrt_complex_and_negative(provider: ArithmeticProvider):
    complex_result = provider._sqrt([Scalar(complex(4, 0))], None)
    assert isinstance(complex_result.value, complex)

    negative_result = provider._sqrt([Scalar(-4)], None)
    assert isinstance(negative_result.value, complex)

    with pytest.raises(builtins.TypeError):
        provider._sqrt([Scalar("not-a-number")], None)


def test_log_variants_and_errors(provider: ArithmeticProvider):
    complex_log = provider._log([Scalar(complex(1, 1))], None)
    assert isinstance(complex_log.value, complex)

    with pytest.raises(ArgumentError):
        provider._log([Scalar(0)], None)

    with pytest.raises(builtins.TypeError):
        provider._log([Scalar("bad")], None)

    complex_log10 = provider._log10([Scalar(complex(1, 1))], None)
    assert isinstance(complex_log10.value, complex)

    with pytest.raises(ArgumentError):
        provider._log10([Scalar(-1)], None)

    with pytest.raises(builtins.TypeError):
        provider._log10([Scalar("bad")], None)


def test_round_with_invalid_decimals(provider: ArithmeticProvider):
    result = provider._round([Scalar(1.2345), Scalar(2)], None)
    assert math.isclose(result.value, 1.23, rel_tol=0, abs_tol=1e-9)

    with pytest.raises((ValueError, builtins.TypeError)):
        provider._round([Scalar(1.2), Scalar("two")], None)


def test_exp_and_abs_and_rounding_errors(provider: ArithmeticProvider):
    with pytest.raises(builtins.TypeError):
        provider._abs([Scalar("bad")], None)

    complex_exp = provider._exp([Scalar(complex(0, 1))], None)
    assert isinstance(complex_exp.value, complex)

    with pytest.raises(builtins.TypeError):
        provider._exp([Scalar("bad")], None)

    with pytest.raises(builtins.TypeError):
        provider._floor([Scalar("bad")], None)

    with pytest.raises(builtins.TypeError):
        provider._ceiling([Scalar("bad")], None)


def test_min_max_and_random(provider: ArithmeticProvider, monkeypatch):
    with pytest.raises(ArgumentError):
        provider._min([], None)
    with pytest.raises(builtins.TypeError):
        provider._min([Scalar(1), Scalar("bad")], None)

    with pytest.raises(ArgumentError):
        provider._max([], None)
    with pytest.raises(builtins.TypeError):
        provider._max([Scalar(1), Scalar("bad")], None)

    # Random without args uses random.random
    monkeypatch.setattr(random, "random", lambda: 0.5)
    assert provider._random([], None).value == 0.5

    # Random with single scalar integer bounds
    monkeypatch.setattr(random, "randint", lambda a, b: b)
    assert provider._random([Scalar(3)], None).value == 2

    with pytest.raises((ValueError, builtins.TypeError)):
        provider._random([Scalar("bad")], None)

    with pytest.raises(builtins.TypeError):
        provider._random([Scalar(1), Scalar("bad")], None)

    monkeypatch.setattr(random, "uniform", lambda a, b: (a + b) / 2)
    assert provider._random([Scalar(1), Scalar(3)], None).value == 2
