from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from model_bakery import baker
from core.models import Bucket
from transactions.models import Transaction
from transactions.models import Category
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
    assert transaction.split_income in [True, False]
    assert transaction.user.pk is not None


@pytest.mark.django_db
def test_crud_transaction(
    transaction_recipe: str,
    category_recipe: str,
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
    new_category = baker.make_recipe(
        category_recipe,
        name="New Income Category",
        sign=Category.Sign.POSITIVE
    )
    transaction.category = new_category
    transaction.save()
    updated_transaction = Transaction.objects.get(pk=transaction.pk)
    assert str(updated_transaction.category) == str(new_category)
    assert updated_transaction.category.sign == Category.Sign.POSITIVE

    # Delete
    transaction.delete()
    assert Transaction.objects.count() == 0


@pytest.mark.django_db
def test_str_method(transaction: Transaction):
    """Test the string representation of the model"""
    assert str(transaction) ==f"{truncate(str(transaction.description), 15)}: {transaction.amount}"


@pytest.mark.django_db
def test_full_info_method(transaction: Transaction):
    """Test the full info method of the model"""
    assert transaction.get_full_info() == f"{transaction.date}, {transaction.category.name}, {truncate(str(transaction.description), 10)}, {transaction.location}, {transaction.bucket}"


@pytest.mark.django_db
def test_split_income(
    user_recipe: str,
    location_recipe: str,
    bucket_recipe: str,
    category_recipe: str,
    transaction_recipe: str,
):
    """Test the _split_income method splits a transaction correctly based on bucket allocations."""

    user = baker.make_recipe(user_recipe)
    location = baker.make_recipe(location_recipe, user=user)
    baker.make_recipe(bucket_recipe, user=user, name="Bucket1", allocation_percentage=60)
    baker.make_recipe(bucket_recipe, user=user, name="Bucket2", allocation_percentage=40)
    category = baker.make_recipe(category_recipe, sign=Category.Sign.POSITIVE)
    amount = Decimal("100.00")
    parent_transaction = baker.make_recipe(
        transaction_recipe,
        category=category,
        location=location,
        amount=amount,
        description="Test Income",
        split_income=True,
        date=now,
        user=user,
    )

    parent_transaction._split_income()
    split_transactions = Transaction.objects.filter(parent_transaction=parent_transaction)
    assert split_transactions.count() == 2
    amounts = [transaction.amount for transaction in split_transactions]
    assert Decimal("60.00") in amounts
    assert Decimal("40.00") in amounts
    assert sum(amounts) == amount
    parent_transaction.refresh_from_db()
    assert parent_transaction.amount == 0
    assert parent_transaction.description == f"Test Income ({amount})"

    for transaction in split_transactions:
        assert transaction.user == parent_transaction.user
        assert transaction.category == parent_transaction.category
        assert transaction.date == parent_transaction.date
        assert transaction.location == parent_transaction.location
        assert transaction.split_income is False
        assert transaction.parent_transaction == parent_transaction
        bucket_percentage = transaction.bucket.allocation_percentage
        assert f"({bucket_percentage}%)" in transaction.description
        expected_amount = (amount * Decimal(str(bucket_percentage)) / Decimal("100")).quantize(Decimal(".01"))
        assert transaction.amount == expected_amount


@pytest.mark.django_db
def test_validate_user(transaction_recipe: str, user_recipe: str):
    """Test validating the user field"""
    user = baker.make_recipe(user_recipe)
    good_transaction = baker.make_recipe(transaction_recipe, user=user)
    good_transaction.validate_user()

    bad_transaction = baker.make_recipe(transaction_recipe)
    bad_transaction.user = None
    with pytest.raises(ValidationError):
        bad_transaction.validate_user()


@pytest.mark.django_db
def test_validate_bucket(
    user_recipe: str,
    category_recipe: str,
    bucket_recipe: str,
    transaction_recipe: str,
):
    """Test validating the bucket field"""
    user = baker.make_recipe(user_recipe)
    bucket = baker.make_recipe(bucket_recipe, user=user, allocation_percentage=100)

    positive_category = baker.make_recipe(category_recipe, sign=Category.Sign.POSITIVE)
    negative_category = baker.make_recipe(category_recipe, sign=Category.Sign.NEGATIVE)

    positive_transaction = baker.prepare_recipe(
        transaction_recipe,
        category=positive_category,
        split_income=False,
        bucket=None
    )
    with pytest.raises(ValidationError):
        positive_transaction.validate_bucket()

    positive_split_transaction = baker.make_recipe(
        transaction_recipe,
        category=positive_category,
        split_income=True,
        bucket=None,
        user=user,
    )
    positive_split_transaction.validate_bucket()

    negative_transaction = baker.make_recipe(
        transaction_recipe,
        category=negative_category,
        bucket=bucket,
        user=user,
    )
    negative_transaction.validate_bucket()

    negative_transaction_no_bucket = baker.prepare_recipe(
        transaction_recipe,
        category=negative_category,
        bucket=None,
        user=user,
    )
    with pytest.raises(ValidationError):
        negative_transaction_no_bucket.validate_bucket()


@pytest.mark.django_db
def test_validate_split_income(
    user_recipe: str,
    category_recipe: str,
    bucket_recipe: str,
    transaction_recipe: str,
):
    """Test validating split_income field."""

    user = baker.make_recipe(user_recipe)

    positive_category = baker.make_recipe(category_recipe, sign=Category.Sign.POSITIVE)
    negative_category = baker.make_recipe(category_recipe, sign=Category.Sign.NEGATIVE)
    neutral_category = baker.make_recipe(category_recipe, sign=Category.Sign.NEUTRAL)

    # Test 1: Positive transaction with split but incomplete allocation
    baker.make_recipe(bucket_recipe, user=user, allocation_percentage=60)
    positive_transaction = baker.prepare_recipe(
        transaction_recipe,
        category=positive_category,
        split_income=True,
        user=user,
    )
    with pytest.raises(ValidationError):
        positive_transaction.validate_split_income()

    # Test 2: Positive transaction with split and complete allocation
    Bucket.available_objects.all().delete()
    baker.make_recipe(bucket_recipe, user=user, allocation_percentage=60)
    baker.make_recipe(bucket_recipe, user=user, allocation_percentage=40)
    positive_transaction_complete = baker.prepare_recipe(
        transaction_recipe,
        category=positive_category,
        split_income=True,
        user=user,
    )
    positive_transaction_complete.validate_split_income()

    # Test 3: Negative transaction with split
    negative_transaction = baker.prepare_recipe(
        transaction_recipe,
        category=negative_category,
        split_income=True,
        user=user,
    )
    with pytest.raises(ValidationError):
        negative_transaction.validate_split_income()

    # Test 4: Neutral transaction with split
    neutral_transaction = baker.prepare_recipe(
        transaction_recipe,
        category=neutral_category,
        split_income=True,
        user=user,
    )
    with pytest.raises(ValidationError):
        neutral_transaction.validate_split_income()

    # Test 5: Positive transaction without split (should pass regardless of allocation)
    Bucket.available_objects.all().delete()
    positive_no_split = baker.prepare_recipe(
        transaction_recipe,
        category=positive_category,
        split_income=False,
        user=user,
    )
    positive_no_split.validate_split_income()


@pytest.mark.django_db
def test_meta_class(transaction_recipe: str):
    """Test the meta options"""
    transaction = baker.prepare_recipe(transaction_recipe)
    assert transaction._meta.verbose_name == "Transaction"
    assert transaction._meta.verbose_name_plural == "Transactions"
    assert transaction._meta.ordering == ("-date",)
