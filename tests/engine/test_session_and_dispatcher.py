"""Session and dispatcher coverage tests."""

from mathlang.engine import dispatcher
from mathlang.engine.session import Session
from mathlang.types.scalar import Scalar


def test_dispatcher_exports_operations():
    """Dispatcher re-exports registry helpers."""
    op = dispatcher.get_operation("Abs")
    assert op is not None
    assert op.identifier == "Abs"
    assert any(o.identifier == "Abs" for o in dispatcher.list_operations())


def test_session_scope_and_management():
    parent = Session()
    child = parent.create_child()

    parent.set("x", Scalar(1))
    child.set("y", Scalar(2))

    assert child.get("x").value == 1
    assert child.has("y")
    assert not child.has("z")

    assert child.delete("y") is True
    assert child.delete("y") is False

    child.set("temp", Scalar(3))
    assert "temp" in child.list_variables()

    child.clear()
    assert child.list_variables() == {"x": parent.get("x")}
