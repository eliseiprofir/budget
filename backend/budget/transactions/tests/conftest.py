import pytest
from model_bakery import baker
from transactions.models import Category
from transactions.models import Transaction


@pytest.fixture
def category(category_recipe) -> Category:
    """Fixture for creating a Category instance."""
    return baker.make_recipe(category_recipe)


@pytest.fixture
def transaction(transaction_recipe) -> Transaction:
    """Fixture for creating a Transaction instance."""
    return baker.make_recipe(transaction_recipe)
