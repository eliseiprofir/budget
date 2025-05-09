import pytest
from model_bakery import baker
from rest_framework.test import APIRequestFactory

from transactions.models import Transaction
from transactions.serializers import TransactionListSerializer
from transactions.serializers import TransactionDetailSerializer
from transactions.serializers import TransactionWriteSerializer


@pytest.mark.django_db
def test_list_serializer_create(transaction_recipe: str):
    """Test that the TransactionListSerializer reads the data correctly."""
    factory = APIRequestFactory()
    request = factory.get('/')
    transaction = baker.make_recipe(transaction_recipe)
    serializer = TransactionListSerializer(transaction, context={"request": request})
    assert serializer.data["id"] == str(transaction.id)
    assert serializer.data["description"] == transaction.description
    assert serializer.data["category"] is not None
    assert serializer.data["date"] is not None
    assert serializer.data["amount"] is not None
    assert serializer.data["location"] is not None
    assert serializer.data["bucket"] is not None
    assert serializer.data["split_income"] is not None
    assert serializer.data["user"] is not None
    assert isinstance(serializer.data["user"], str)
    assert "/api/users/" in serializer.data["user"]


@pytest.mark.django_db
def test_detail_serializer_create(
    transaction_recipe: str,
    user_recipe: str,
    category_recipe: str,
    location_recipe: str,
    bucket_recipe: str,
):
    """Test that the TransactionDetailSerializer reads the data correctly."""
    factory = APIRequestFactory()
    request = factory.get('/')
    user = baker.make_recipe(user_recipe)
    category = baker.make_recipe(category_recipe)
    location = baker.make_recipe(location_recipe)
    bucket = baker.make_recipe(bucket_recipe)
    transaction = baker.make_recipe(
        transaction_recipe,
        category=category,
        location=location,
        bucket=bucket,
        user=user,
    )
    serializer = TransactionDetailSerializer(transaction, context={"request": request})
    assert serializer.data["id"] == str(transaction.id)
    assert serializer.data["description"] == transaction.description
    assert serializer.data["category"]["id"] == str(category.id)
    assert serializer.data["date"].split("T")[0] == str(transaction.date).split(" ")[0]
    assert str(serializer.data["amount"]) == str(transaction.amount)
    assert serializer.data["location"]["id"] == str(location.id)
    assert serializer.data["bucket"]["id"] == str(bucket.id)
    assert serializer.data["split_income"] == transaction.split_income
    assert serializer.data["user"]["id"] == str(user.id)


@pytest.mark.django_db
def test_write_serializer_create(
    user_recipe: str,
    category_recipe: str,
    location_recipe: str,
    bucket_recipe: str,
    transaction_recipe: str,
):
    """Test the TransactionWriteSerializer create method"""
    user = baker.make_recipe(user_recipe)
    category = baker.make_recipe(category_recipe, user=user)
    location = baker.make_recipe(location_recipe, user=user)
    bucket = baker.make_recipe(bucket_recipe, user=user, allocation_percentage=100)
    transaction = baker.prepare_recipe(
        transaction_recipe,
        category=category,
        location=location,
        bucket=bucket,
        user=user,
    )
    data = {
        "description": transaction.description,
        "category": category.pk,
        "amount": transaction.amount,
        "date": transaction.date,
        "location": location.pk,
        "bucket": bucket.pk,
    }
    mock_request = type("Request", (), {"user": user})()
    serializer = TransactionWriteSerializer(data=data, context={"request": mock_request})
    assert serializer.is_valid(), serializer.errors
    serialized_data = serializer.save(user=user)
    assert serialized_data.description == transaction.description
    assert serialized_data.category.pk == category.pk
    assert serialized_data.date == transaction.date
    assert serialized_data.amount == transaction.amount
    assert serialized_data.location.pk == location.pk
    assert serialized_data.bucket.pk == bucket.pk


@pytest.mark.django_db
def test_write_serializer_update(
    transaction: Transaction,
    category_recipe: str,
    location_recipe: str,
    bucket_recipe: str,
):
    """Test the TransactionWriteSerializer update method"""
    original_user = transaction.user
    category = baker.make_recipe(category_recipe, name="New Category", user=original_user)
    location = baker.make_recipe(location_recipe, name="New Location", user=original_user)
    bucket = baker.make_recipe(bucket_recipe, name="New Bucket", user=original_user, allocation_percentage=100)
    data = {
        "description": transaction.description,
        "category": str(category.id),
        "date": transaction.date,
        "amount": transaction.amount,
        "bucket": str(bucket.id),
        "location": str(location.id),
    }
    mock_request = type("Request", (), {"user": original_user})()
    serializer = TransactionWriteSerializer(transaction, data=data, context={"request": mock_request})
    assert serializer.is_valid(), serializer.errors
    updated_transaction = serializer.save()
    assert updated_transaction.user == original_user
    assert updated_transaction.description == data["description"]
    assert str(updated_transaction.category.pk) == data["category"]
    assert updated_transaction.date == data["date"]
    assert updated_transaction.amount == data["amount"]
    assert str(updated_transaction.bucket.pk) == data["bucket"]
    assert str(updated_transaction.location.pk) == data["location"]
