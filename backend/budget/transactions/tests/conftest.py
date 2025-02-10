import pytest
from model_bakery import baker
from transactions.models import TransactionType
from transactions.models import Category


@pytest.fixture
def transaction_type(transaction_type_recipe) -> TransactionType:
    """Fixture for creating a TransactionType instance."""
    return baker.make_recipe(transaction_type_recipe)


@pytest.fixture
def category(category_recipe) -> Category:
    """Fixture for creating a Category instance."""
    return baker.make_recipe(category_recipe)
