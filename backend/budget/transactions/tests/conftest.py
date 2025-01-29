import pytest
from model_bakery import baker
from transactions.models import Category


@pytest.fixture
def category(category_recipe) -> Category:
    """Fixture for creating a Category instance."""
    return baker.make_recipe(category_recipe)
