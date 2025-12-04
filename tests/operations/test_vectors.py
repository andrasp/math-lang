"""Tests for vector operations."""

import math
import pytest
from mathlang.engine import evaluate
from mathlang.engine.session import Session
from mathlang.engine.errors import ArgumentError
from mathlang.types.scalar import Scalar
from mathlang.types.vector import Vector


class TestVectorCreationExtended:
    """Extended tests for vector creation operations."""

    def test_zero_vec(self):
        session = Session()
        results = evaluate("ZeroVec(3)", session)
        assert isinstance(results[0].value, Vector)
        assert results[0].value.values == [0.0, 0.0, 0.0]

    def test_zero_vec_dimension_5(self):
        session = Session()
        results = evaluate("ZeroVec(5)", session)
        assert len(results[0].value) == 5
        assert all(v == 0.0 for v in results[0].value.values)

    def test_unit_vec_x_axis(self):
        session = Session()
        results = evaluate("UnitVec(3, 0)", session)
        assert results[0].value.values == [1.0, 0.0, 0.0]

    def test_unit_vec_y_axis(self):
        session = Session()
        results = evaluate("UnitVec(3, 1)", session)
        assert results[0].value.values == [0.0, 1.0, 0.0]

    def test_unit_vec_z_axis(self):
        session = Session()
        results = evaluate("UnitVec(3, 2)", session)
        assert results[0].value.values == [0.0, 0.0, 1.0]


class TestVectorAngle:
    """Tests for vector angle calculation."""

    def test_angle_orthogonal(self):
        session = Session()
        results = evaluate("VecAngle(Vec(1, 0, 0), Vec(0, 1, 0))", session)
        assert abs(results[0].value.value - math.pi / 2) < 0.0001

    def test_angle_parallel(self):
        session = Session()
        results = evaluate("VecAngle(Vec(1, 0), Vec(2, 0))", session)
        assert abs(results[0].value.value) < 0.0001

    def test_angle_opposite(self):
        session = Session()
        results = evaluate("VecAngle(Vec(1, 0), Vec(-1, 0))", session)
        assert abs(results[0].value.value - math.pi) < 0.0001

    def test_angle_45_degrees(self):
        session = Session()
        results = evaluate("VecAngle(Vec(1, 0), Vec(1, 1))", session)
        assert abs(results[0].value.value - math.pi / 4) < 0.0001


class TestVectorComponent:
    """Tests for vector component access."""

    def test_get_first_component(self):
        session = Session()
        results = evaluate("VecComponent(Vec(1, 2, 3), 0)", session)
        assert results[0].value.value == 1.0

    def test_get_middle_component(self):
        session = Session()
        results = evaluate("VecComponent(Vec(1, 2, 3), 1)", session)
        assert results[0].value.value == 2.0

    def test_get_last_component(self):
        session = Session()
        results = evaluate("VecComponent(Vec(1, 2, 3), 2)", session)
        assert results[0].value.value == 3.0


class TestVectorProjection:
    """Tests for vector projection."""

    def test_projection_onto_x_axis(self):
        session = Session()
        results = evaluate("Projection(Vec(3, 4), Vec(1, 0))", session)
        assert results[0].value.values == [3.0, 0.0]

    def test_projection_onto_y_axis(self):
        session = Session()
        results = evaluate("Projection(Vec(3, 4), Vec(0, 1))", session)
        assert results[0].value.values == [0.0, 4.0]

    def test_projection_onto_same_direction(self):
        session = Session()
        results = evaluate("Projection(Vec(2, 0), Vec(4, 0))", session)
        assert results[0].value.values[0] == pytest.approx(2.0)


class TestVectorErrors:
    """Tests for vector operation error handling."""

    def test_cross_product_wrong_dimension(self):
        session = Session()
        with pytest.raises(ArgumentError, match="3D vectors"):
            evaluate("CrossProduct(Vec(1, 2), Vec(3, 4))", session)

    def test_dot_product_dimension_mismatch(self):
        session = Session()
        with pytest.raises(ArgumentError, match="same dimension"):
            evaluate("DotProduct(Vec(1, 2), Vec(1, 2, 3))", session)

    def test_normalize_zero_vector(self):
        session = Session()
        with pytest.raises(ArgumentError, match="zero vector"):
            evaluate("Normalize(Vec(0, 0, 0))", session)

    def test_angle_with_zero_vector(self):
        session = Session()
        with pytest.raises(ArgumentError, match="zero vector"):
            evaluate("VecAngle(Vec(1, 0), Vec(0, 0))", session)

    def test_vec_add_dimension_mismatch(self):
        session = Session()
        with pytest.raises(ArgumentError, match="same dimension"):
            evaluate("VecAdd(Vec(1, 2), Vec(1, 2, 3))", session)

    def test_vec_sub_dimension_mismatch(self):
        session = Session()
        with pytest.raises(ArgumentError, match="same dimension"):
            evaluate("VecSub(Vec(1, 2), Vec(1, 2, 3))", session)

    def test_projection_dimension_mismatch(self):
        session = Session()
        with pytest.raises(ArgumentError, match="same dimension"):
            evaluate("Projection(Vec(1, 2), Vec(1, 2, 3))", session)

    def test_projection_onto_zero_vector(self):
        session = Session()
        with pytest.raises(ArgumentError, match="zero vector"):
            evaluate("Projection(Vec(1, 2), Vec(0, 0))", session)

    def test_vec_component_out_of_range(self):
        session = Session()
        with pytest.raises(ArgumentError, match="out of range"):
            evaluate("VecComponent(Vec(1, 2, 3), 5)", session)

    def test_zero_vec_negative_dimension(self):
        session = Session()
        with pytest.raises(ArgumentError, match="positive"):
            evaluate("ZeroVec(-1)", session)

    def test_unit_vec_invalid_axis(self):
        session = Session()
        with pytest.raises(ArgumentError, match="out of range"):
            evaluate("UnitVec(3, 5)", session)

    def test_unit_vec_negative_dimension(self):
        session = Session()
        with pytest.raises(ArgumentError, match="positive"):
            evaluate("UnitVec(-1, 0)", session)
