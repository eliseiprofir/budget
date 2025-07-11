import pytest

from rest_framework.test import APIClient
from accounts.tests.conftest import user  #noqa: F401


@pytest.fixture
def apiclient() -> APIClient:
    """Fixture for creating an unauthenticated APIClient."""
    return APIClient()


@pytest.fixture
def authenticated_apiclient(user) -> APIClient:  # noqa: F811
    """Fixture for creating an authenticated APIClient."""
    client = APIClient()
    client.force_authenticate(user=user)
    yield client
    client.force_authenticate(user=None)


@pytest.fixture
def admin_apiclient(admin_user) -> APIClient:
    """Fixture for creating an authenticated admin API client."""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    yield client
    client.force_authenticate(user=None)


@pytest.fixture
def user_recipe() -> str:
    """Fixture for creating a User recipe"""
    return "accounts.tests.user_recipe"


@pytest.fixture
def admin_user_recipe() -> str:
    """Fixture for creating an admin User recipe"""
    return "accounts.tests.admin_user_recipe"


@pytest.fixture
def location_recipe() -> str:
    """Fixture for creating a Location recipe"""
    return "core.tests.location_recipe"


@pytest.fixture
def bucket_recipe() -> str:
    """Fixture for creating a Bucket recipe"""
    return "core.tests.bucket_recipe"


@pytest.fixture
def category_recipe() -> str:
    """Fixture for creating a Category recipe"""
    return "transactions.tests.category_recipe"


@pytest.fixture
def transaction_recipe() -> str:
    """Fixture for creating a Transaction recipe"""
    return "transactions.tests.transaction_recipe"


@pytest.fixture
def positive_category_recipe() -> str:
    """Fixture for creating a positive Category recipe"""
    return "transactions.tests.positive_category_recipe"


@pytest.fixture
def positive_transaction_recipe() -> str:
    """Fixture for creating a positive Transaction recipe"""
    return "transactions.tests.positive_transaction_recipe"


@pytest.fixture
def negative_category_recipe() -> str:
    """Fixture for creating a negative Category recipe"""
    return "transactions.tests.negative_category_recipe"


@pytest.fixture
def negative_transaction_recipe() -> str:
    """Fixture for creating a negative Transaction recipe"""
    return "transactions.tests.negative_transaction_recipe"


@pytest.fixture
def neutral_category_recipe() -> str:
    """Fixture for creating a neutral Category recipe"""
    return "transactions.tests.neutral_category_recipe"


@pytest.fixture
def neutral_transaction_recipe() -> str:
    """Fixture for creating a neutral Transaction recipe"""
    return "transactions.tests.neutral_transaction_recipe"