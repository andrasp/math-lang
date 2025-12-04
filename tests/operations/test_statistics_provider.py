"""Additional coverage for StatisticsProvider operations."""

import pytest

from mathlang.engine.errors import ArgumentError, TypeError
from mathlang.operations.providers.statistics import StatisticsProvider
from mathlang.types.collection import Interval, List
from mathlang.types.scalar import Scalar


@pytest.fixture
def provider() -> StatisticsProvider:
    return StatisticsProvider()


def test_extract_numbers_validations(provider: StatisticsProvider):
    with pytest.raises(TypeError):
        provider._extract_numbers(Scalar(1))

    with pytest.raises(TypeError):
        provider._extract_numbers(List([Scalar("bad")]))

    interval_values = provider._extract_numbers(Interval(0, 3, 1))
    assert interval_values == [0, 1, 2]


def test_central_tendency_errors(provider: StatisticsProvider):
    with pytest.raises(ArgumentError):
        provider._mean([List([])], None)

    with pytest.raises(ArgumentError):
        provider._median([List([])], None)

    with pytest.raises(ArgumentError):
        provider._mode([List([])], None)


def test_variance_and_stddev_paths(provider: StatisticsProvider):
    values = List([Scalar(1)])
    with pytest.raises(ArgumentError):
        provider._variance([values], None)

    with pytest.raises(ArgumentError):
        provider._pop_variance([values], None)

    with pytest.raises(ArgumentError):
        provider._stddev([values], None)

    with pytest.raises(ArgumentError):
        provider._pop_stddev([values], None)


def test_relationship_metrics(provider: StatisticsProvider):
    list1 = List([Scalar(1), Scalar(2)])
    list2 = List([Scalar(1)])
    with pytest.raises(ArgumentError):
        provider._correlation([list1, list2], None)

    with pytest.raises(ArgumentError):
        provider._covariance([list1, list2], None)

    identical = List([Scalar(1), Scalar(1)])
    zero_var = provider._correlation([list1, identical], None)
    assert zero_var.value == 0.0

    with pytest.raises(ArgumentError):
        provider._linear_regression([identical, identical], None)


def test_percentiles_and_quartiles(provider: StatisticsProvider):
    values = List([Scalar(1), Scalar(2), Scalar(3), Scalar(4)])

    with pytest.raises(TypeError):
        provider._percentile([values, List([])], None)

    with pytest.raises(ArgumentError):
        provider._percentile([values, Scalar(-1)], None)

    with pytest.raises(ArgumentError):
        provider._percentile([values, Scalar(101)], None)

    assert provider._percentile([values, Scalar(0)], None).value == 1
    assert provider._percentile([values, Scalar(100)], None).value == 4

    mid = provider._percentile([values, Scalar(50)], None).value
    assert mid == 2.5

    with pytest.raises(ArgumentError):
        provider._quartiles([List([])], None)

    quartiles = provider._quartiles([values], None)
    assert [q.value for q in quartiles] == [1.75, 2.5, 3.25]

    with pytest.raises(ArgumentError):
        provider._iqr([List([])], None)

    iqr = provider._iqr([values], None)
    assert iqr.value == 1.5
