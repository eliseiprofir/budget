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
    assert serializer.data["user"] is not None
    assert serializer.data["description"] == transaction.description
    assert serializer.data["category"] is not None
    assert serializer.data["date"] is not None
    assert serializer.data["amount"] is not None
    assert serializer.data["location"] is not None
    assert serializer.data["bucket"] is not None
    assert serializer.data["transaction_type"] is not None
    assert "/api/users/" in serializer.data["user"]
    assert isinstance(serializer.data["user"], str)
    assert "/api/categories/" in serializer.data["category"]
    assert isinstance(serializer.data["location"], str)
    assert "/api/locations/" in serializer.data["location"]
    assert isinstance(serializer.data["bucket"], str)
    assert "/api/buckets/" in serializer.data["bucket"]


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
        user=user,
        category=category,
        location=location,
        bucket=bucket,
    )
    serializer = TransactionDetailSerializer(transaction, context={"request": request})
    assert serializer.data["id"] == str(transaction.id)
    assert serializer.data["user"]["id"] == str(user.id)
    assert serializer.data["description"] == transaction.description
    assert serializer.data["category"]["id"] == str(category.id)
    assert serializer.data["date"] == transaction.date
    assert str(serializer.data["amount"]) == str(transaction.amount)
    assert serializer.data["location"]["id"] == str(location.id)
    assert serializer.data["bucket"]["id"] == str(bucket.id)
    assert serializer.data["transaction_type"] == transaction.transaction_type


@pytest.mark.django_db
def test_write_serializer_create(
    transaction_recipe: str,
    user_recipe: str,
    category_recipe: str,
    location_recipe: str,
    bucket_recipe: str,
):
    """Test the TransactionWriteSerializer create method"""
    user = baker.make_recipe(user_recipe)
    category = baker.make_recipe(category_recipe)
    location = baker.make_recipe(location_recipe)
    bucket = baker.make_recipe(bucket_recipe)
    transaction = baker.prepare_recipe(
        transaction_recipe,
        user=user,
        category=category,
        location=location,
        bucket=bucket,
    )
    data = {
        "user": user.id,
        "description": transaction.description,
        "category": category.pk,
        "amount": transaction.amount,
        "date": transaction.date,
        "location": location.pk,
        "bucket": bucket.pk,
    }
    serializer = TransactionWriteSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    serialized_data = serializer.save()
    assert serialized_data.user.pk == user.pk
    assert serialized_data.description == transaction.description
    assert serialized_data.category.pk == category.pk
    assert str(serialized_data.date) == transaction.date
    assert serialized_data.amount == transaction.amount
    assert serialized_data.location.pk == location.pk
    assert serialized_data.bucket.pk == bucket.pk
    assert serialized_data.transaction_type == transaction.transaction_type


@pytest.mark.django_db
def test_write_serializer_update(
        transaction: Transaction,
        user_recipe: str,
        category_recipe: str,
        location_recipe: str,
        bucket_recipe: str,
):
    """Test the TransactionWriteSerializer update method"""
    user = baker.make_recipe(user_recipe, email="test@gmail.com")
    category = baker.make_recipe(category_recipe, name="New Category")
    location = baker.make_recipe(location_recipe, name="New Location")
    bucket = baker.make_recipe(bucket_recipe, name="New Bucket")
    data = {
        "user": str(user.id),
        "description": transaction.description,
        "category": str(category.id),
        "date": transaction.date,
        "amount": transaction.amount,
        "bucket": str(bucket.id),
        "location": str(location.id),
        "transaction_type": str(category.transaction_type),
    }
    serializer = TransactionWriteSerializer(transaction, data=data)
    assert serializer.is_valid(), serializer.errors
    updated_transaction = serializer.save()
    assert str(updated_transaction.user.pk) == data["user"]
    assert updated_transaction.description == data["description"]
    assert str(updated_transaction.category.pk) == data["category"]
    assert str(updated_transaction.date) == data["date"]
    assert updated_transaction.amount == data["amount"]
    assert str(updated_transaction.bucket.pk) == data["bucket"]
    assert str(updated_transaction.location.pk) == data["location"]
    assert updated_transaction.transaction_type == data["transaction_type"]

