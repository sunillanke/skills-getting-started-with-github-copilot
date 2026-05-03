"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from src.app import app
import src.app as app_module
from tests.test_data import TEST_ACTIVITIES
import copy


@pytest.fixture
def reset_activities():
    """Reset app activities to test data before each test."""
    # Arrange: Reset to known test state
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(TEST_ACTIVITIES))
    yield
    # Cleanup after test
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(TEST_ACTIVITIES))


@pytest.fixture
def client(reset_activities):
    """Provide TestClient with reset activities."""
    # Arrange: Client is ready with fresh test data
    return TestClient(app)
