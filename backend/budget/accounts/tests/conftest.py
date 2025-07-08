import pytest
from model_bakery import baker
from accounts.models import User


@pytest.fixture
def user(user_recipe) -> User:
    """Fixture for creating a User instance."""
    return baker.make_recipe(user_recipe)


@pytest.fixture
def admin_user(admin_user_recipe) -> User:
    """Fixture for creating an Superadmin User instance."""
    return baker.make_recipe(admin_user_recipe)
