"""Coverage-focused tests for type helpers."""

from datetime import datetime

import pytest

from mathlang.engine.session import Session
from mathlang.lang.ast import NumberLiteral
from mathlang.types.callable import Lambda, Thunk
from mathlang.types.coercion import coerce_numeric, is_numeric, is_truthy
from mathlang.types.collection import Interval, List
from mathlang.types.scalar import Scalar


def test_lambda_and_thunk_display(session: Session):
    zero_param = Lambda([], NumberLiteral(1))
    single_param = Lambda(["x"], NumberLiteral(2))
    multi_param = Lambda(["x", "y"], NumberLiteral(3))

    assert zero_param.display() == "() -> 1"
    assert single_param.display() == "x -> 2"
    assert multi_param.display() == "(x, y) -> 3"

    thunk = Thunk(NumberLiteral(5), session)
    assert thunk.display() == "<deferred>"
    assert thunk.force().value == 5


def test_coercion_helpers():
    assert coerce_numeric(Scalar(1), Scalar(2.5)) == (1.0, 2.5)
    assert coerce_numeric(Scalar(1), Scalar(complex(1, 1))) == (1 + 0j, 1 + 1j)
    assert coerce_numeric(Scalar(1), Scalar(2)) == (1, 2)

    assert is_numeric(Scalar(1))
    assert is_numeric(Scalar(1.0))
    assert not is_numeric(Scalar(True))

    assert is_truthy(Scalar(True)) is True
    assert is_truthy(Scalar(False)) is False
    assert is_truthy(Scalar(0)) is False
    assert is_truthy(Scalar(0.0)) is False
    assert is_truthy(Scalar(0j)) is False
    assert is_truthy(Scalar("")) is False
    assert is_truthy(Scalar("x")) is True
    assert is_truthy([]) is False


def test_list_and_interval_behaviour():
    items = [Scalar(i) for i in range(3)]
    lst = List(items)
    assert len(lst) == 3
    assert lst[1].value == 1
    assert lst[-1].value == 2
    assert lst.display() == "[0, 1, 2]"
    assert repr(lst).startswith("List([")
    assert lst.type_name == "List (3 items)"

    long_items = List([Scalar(i) for i in range(12)])
    assert "..." in long_items.display()

    with pytest.raises(IndexError):
        _ = lst[5]

    interval = Interval(0, 5, 2)
    assert interval.start == 0
    assert interval.end == 5
    assert interval.step == 2
    assert len(interval) == 3
    assert interval[1].value == 2
    assert interval[-1].value == 4
    assert interval.to_list() == [0, 2, 4]
    assert interval.display() == "[0..5 step 2)"

    descending = Interval(5, 0, -2)
    assert len(descending) == 3
    assert descending.to_list() == [5, 3, 1]
    assert "step" in descending.display()
    assert [v.value for v in descending] == [5, 3, 1]

    with pytest.raises(IndexError):
        _ = interval[10]

    empty_forward = Interval(5, 5)
    assert len(empty_forward) == 0

    empty_backward = Interval(0, 1, -1)
    assert len(empty_backward) == 0
    assert repr(empty_backward) == "Interval(0, 1, step=-1)"


def test_scalar_display_and_types():
    assert Scalar(True).type_name == "Boolean"
    assert Scalar(1).type_name == "Integer"
    assert Scalar(1.5).type_name == "Float"
    assert Scalar(complex(1, -2)).type_name == "Complex"
    assert Scalar("x").type_name == "String"
    assert Scalar(datetime(2020, 1, 1)).type_name == "DateTime"

    assert Scalar(complex(0, 3)).display() == "3.0i"
    assert Scalar(complex(2, -3)).display() == "2.0 - 3.0i"
    assert Scalar(1.0).display() == "1"
    assert Scalar(False).display() == "false"
    assert Scalar(3).display() == "3"
    assert repr(Scalar(3)) == "Scalar(3)"

    assert Scalar(1) == Scalar(1)
    assert Scalar(1) != Scalar(2)
    assert hash(Scalar(2)) == hash(Scalar(2))

    unknown = Scalar(object())
    assert unknown.type_name == "Unknown"
    assert isinstance((-Scalar(2)).value, int)
    assert (Scalar(2) + Scalar(3)).value == 5
    assert (Scalar(5) - Scalar(2)).value == 3
    assert (Scalar(2) * Scalar(3)).value == 6
    assert (Scalar(8) / Scalar(2)).value == 4
    assert (Scalar(2) ** Scalar(3)).value == 8
