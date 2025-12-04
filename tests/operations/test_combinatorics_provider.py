"""Additional coverage for CombinatoricsProvider operations."""

import pytest

from mathlang.engine.errors import ArgumentError, TypeError
from mathlang.operations.providers.combinatorics import CombinatoricsProvider
from mathlang.types.collection import List
from mathlang.types.scalar import Scalar


@pytest.fixture
def provider() -> CombinatoricsProvider:
    return CombinatoricsProvider()


def test_helper_validations(provider: CombinatoricsProvider):
    with pytest.raises(TypeError):
        provider._get_non_negative_int(Scalar(1.5), "n")
    with pytest.raises(TypeError):
        provider._get_non_negative_int(List([]), "n")
    with pytest.raises(ArgumentError):
        provider._get_non_negative_int(Scalar(-1), "n")

    with pytest.raises(ArgumentError):
        provider._get_positive_int(Scalar(0), "n")

    with pytest.raises(TypeError):
        provider._get_int(Scalar(1.2), "x")


def test_boundary_conditions(provider: CombinatoricsProvider):
    with pytest.raises(ArgumentError):
        provider._factorial([Scalar(171)], None)

    with pytest.raises(ArgumentError):
        provider._permutations([Scalar(3), Scalar(4)], None)

    with pytest.raises(ArgumentError):
        provider._combinations([Scalar(3), Scalar(4)], None)

    with pytest.raises(ArgumentError):
        provider._fibonacci([Scalar(1001)], None)

    with pytest.raises(ArgumentError):
        provider._fibonacci_list([Scalar(0)], None)

    with pytest.raises(ArgumentError):
        provider._fibonacci_list([Scalar(1001)], None)

    with pytest.raises(ArgumentError):
        provider._primes([Scalar(1_000_001)], None)

    assert provider._primes([Scalar(1)], None).items == []
    assert provider._binomial_coeff([Scalar(2), Scalar(3)], None).value == 0


def test_prime_helpers(provider: CombinatoricsProvider):
    factors = provider._prime_factors([Scalar(28)], None)
    assert [item.value for item in factors] == [2, 2, 7]

    assert provider._is_prime([Scalar(2)], None).value == 1
    assert provider._is_prime([Scalar(1)], None).value == 0

    primes = provider._primes([Scalar(10)], None)
    assert [item.value for item in primes] == [2, 3, 5, 7]
