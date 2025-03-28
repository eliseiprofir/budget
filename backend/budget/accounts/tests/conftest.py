import pytest
from model_bakery import baker
from accounts.models import User


@pytest.fixture
def user(user_recipe) -> User:
    """Fixture for creating a User instance."""
    return baker.make_recipe(user_recipe)
