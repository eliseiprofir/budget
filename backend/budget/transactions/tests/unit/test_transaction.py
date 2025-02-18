import pytest
from model_bakery import baker
from transactions.models import Transaction
from transactions.models import TransactionType
from utils.strings import truncate


@pytest.mark.django_db
def test_transaction_creation(transaction_recipe: str):
    """Test creating a Transaction instance with valid data"""
    transaction = baker.make_recipe(transaction_recipe)
    assert transaction.pk is not None
    assert transaction.description != ""
    assert transaction.category.pk is not None
    assert transaction.date != ""
    assert transaction.amount != ""
    assert transaction.location.pk is not None
    assert transaction.bucket.pk is not None
    assert transaction.transaction_type != ""


@pytest.mark.django_db
def test_crud_transaction(
    transaction_recipe: str,
    category_recipe: str,
    transaction_type_recipe: str
):
    """Test the CRUD operations for positive transactions"""

    # Create
    transaction = baker.make_recipe(
        transaction_recipe,
        description="Salary",
        amount=100,
    )
    assert Transaction.objects.count() == 1
    assert transaction.description == "Salary"
    assert transaction.amount == 100

    # Read
    fetched_transaction = Transaction.objects.get(pk=transaction.pk)
    assert fetched_transaction.description == "Salary"
    assert fetched_transaction.amount == 100

    # Update description
    transaction.description = "Bonuses"
    transaction.save()
    updated_transaction = Transaction.objects.get(pk=transaction.pk)
    assert updated_transaction.description == "Bonuses"

    # Update amount
    transaction.amount = 200
    transaction.save()
    updated_transaction = Transaction.objects.get(pk=transaction.pk)
    assert updated_transaction.amount == 200

    # Update category
    new_transaction_type = baker.make_recipe(transaction_type_recipe, sign=TransactionType.Sign.POSITIVE)
    new_category = baker.make_recipe(
        category_recipe,
        name="New Income Category",
        transaction_type=new_transaction_type
    )
    transaction.category = new_category
    transaction.save()
    updated_transaction = Transaction.objects.get(pk=transaction.pk)
    assert str(updated_transaction.category) == str(new_category)
    assert updated_transaction.category.transaction_type.sign == TransactionType.Sign.POSITIVE

    # Delete
    transaction.delete()
    assert Transaction.objects.count() == 0


@pytest.mark.django_db
def test_str_method(transaction: Transaction):
    """Test the string representation of the model"""
    assert f"{truncate(str(transaction.description), 15)}: {transaction.amount}"


@pytest.mark.django_db
def test_full_info_method(transaction: Transaction):
    """Test the full info method of the model"""
    assert f"{transaction.date}, {transaction.transaction_type}, {transaction.category.name}, {truncate(str(transaction.description), 10)}, {transaction.location}, {transaction.bucket}"


@pytest.mark.django_db
def test_meta_class(transaction_recipe: str):
    """Test the meta options"""
    transaction = baker.prepare_recipe(transaction_recipe)
    assert transaction._meta.verbose_name == "Transaction"
    assert transaction._meta.verbose_name_plural == "Transactions"
    assert transaction._meta.ordering == ("-date",)
