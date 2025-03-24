import pytest
from model_bakery import baker


@pytest.mark.django_db
def test_update_transaction_type_on_category_update(
    transaction_type_recipe: str,
    category_recipe: str,
    transaction_recipe: str
):
    """Test that transaction_type is updated when category is set."""
    transaction_type = baker.make_recipe(transaction_type_recipe)
    category = baker.make_recipe(category_recipe, transaction_type=transaction_type)
    transaction = baker.make_recipe(transaction_recipe)

    transaction.category = category
    transaction.save()

    transaction.refresh_from_db()
    assert transaction.transaction_type == str(transaction_type)

