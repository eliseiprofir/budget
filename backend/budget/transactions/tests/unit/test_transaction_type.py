import pytest
from model_bakery import baker
from transactions.models import TransactionType


@pytest.mark.django_db
def test_transaction_type_creation(transaction_type_recipe: str):
    """Test creating a TransactionType instance with valid data"""
    transaction_type = baker.make_recipe(transaction_type_recipe)
    assert transaction_type.pk is not None
    assert transaction_type.name != ""
    assert transaction_type.is_removed in [True, False]


@pytest.mark.django_db
def test_crud_operations(transaction_type_recipe: str):
    """Test the CRUD operations for the model"""

    # Create
    name = "Income"
    transaction_type = baker.make_recipe(
        transaction_type_recipe,
        name=name,
    )
    assert TransactionType.available_objects.count() == 1
    assert transaction_type.name == name

    # Read
    fetched_transaction_type = TransactionType.available_objects.get(pk=transaction_type.pk)
    assert fetched_transaction_type.name == name

    # Update
    transaction_type.name = "Expense"
    transaction_type.save()
    updated_transaction_type = TransactionType.available_objects.get(pk=transaction_type.pk)
    assert updated_transaction_type.name == "Expense"

    # Delete
    transaction_type.delete()
    assert TransactionType.available_objects.count() == 0


@pytest.mark.django_db
def test_str_method(transaction_type: TransactionType):
    """Test the string representation of the model"""
    assert str(transaction_type) == f"{transaction_type.name}"


@pytest.mark.django_db
def test_meta_class(transaction_type_recipe: str):
    """Test the meta options"""
    transaction_type = baker.prepare_recipe(transaction_type_recipe)
    assert transaction_type._meta.verbose_name == "Transaction Type"
    assert transaction_type._meta.verbose_name_plural == "Transaction Types"
    assert transaction_type._meta.ordering == ("name",)
