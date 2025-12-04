"""Pytest configuration and fixtures."""

import pytest

from mathlang.engine.session import Session


@pytest.fixture
def session() -> Session:
    """Create a fresh evaluation session."""
    return Session()
