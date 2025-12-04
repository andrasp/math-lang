"""Tests for the Vector type."""

import pytest
from mathlang.types.vector import Vector
from mathlang.types.scalar import Scalar


class TestVectorCreation:
    """Tests for Vector creation and basic properties."""

    def test_create_int_vector(self):
        v = Vector([1, 2, 3])
        assert len(v) == 3
        assert v.values == [1, 2, 3]

    def test_create_float_vector(self):
        v = Vector([1.0, 2.5, 3.7])
        assert len(v) == 3
        assert v.values == [1.0, 2.5, 3.7]

    def test_create_complex_vector(self):
        v = Vector([1 + 2j, 3 + 4j])
        assert len(v) == 2
        assert v.values == [1 + 2j, 3 + 4j]

    def test_create_empty_vector(self):
        v = Vector([])
        assert len(v) == 0
        assert v.values == []


class TestVectorTypeName:
    """Tests for Vector type_name property."""

    def test_empty_vector_type_name(self):
        v = Vector([])
        assert v.type_name == "Vector (empty)"

    def test_int_vector_type_name(self):
        v = Vector([1, 2, 3])
        assert v.type_name == "Vector (Integer)"

    def test_float_vector_type_name(self):
        v = Vector([1.0, 2.0, 3.0])
        assert v.type_name == "Vector (Float)"

    def test_complex_vector_type_name(self):
        v = Vector([1 + 2j, 3 + 4j])
        assert v.type_name == "Vector (Complex)"


class TestVectorIndexing:
    """Tests for Vector indexing."""

    def test_get_item(self):
        v = Vector([10, 20, 30])
        result = v[0]
        assert isinstance(result, Scalar)
        assert result.value == 10

    def test_get_item_last(self):
        v = Vector([10, 20, 30])
        result = v[2]
        assert result.value == 30

    def test_get_item_negative(self):
        v = Vector([10, 20, 30])
        result = v[-1]
        assert result.value == 30


class TestVectorDisplay:
    """Tests for Vector display method."""

    def test_display_short_vector(self):
        v = Vector([1, 2, 3])
        assert v.display() == "[1, 2, 3]"

    def test_display_exact_10_elements(self):
        v = Vector(list(range(10)))
        result = v.display()
        assert result == "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"

    def test_display_long_vector(self):
        v = Vector(list(range(20)))
        result = v.display()
        # Should show first 5, ..., last 3
        assert "0, 1, 2, 3, 4" in result
        assert "..." in result
        assert "17, 18, 19" in result


class TestVectorRepr:
    """Tests for Vector __repr__ method."""

    def test_repr(self):
        v = Vector([1, 2, 3])
        assert repr(v) == "Vector([1, 2, 3])"
