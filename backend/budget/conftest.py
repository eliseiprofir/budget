import pytest

from rest_framework.test import APIClient
from accounts.tests.conftest import user  # noqa: F401

@pytest.fixture
def apiclient() -> APIClient:
    """Fixture for creating an unauthenticated APIClient."""
    return APIClient()

@pytest.fixture
def authenticated_apiclient(user):
    """Fixture for creating an authenticated APIClient."""
    client = APIClient()
    client.force_authenticate(user=user)
    yield client
    client.force_authenticate(user=None)

@pytest.fixture
def user_recipe() -> str:
    """Fixture for creating a User recipe"""
    return "accounts.tests.user_recipe"

@pytest.fixture
def bucket_recipe() -> str:
    """Fixture for creating a Bucket recipe user"""
    return "core.tests.bucket_recipe"

@pytest.fixture
def location_recipe() -> str:
    """Fixture for creating a Location recipe user"""
    return "core.tests.location_recipe"
