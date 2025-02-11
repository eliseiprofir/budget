import pytest
from model_bakery import baker
from rest_framework.test import APIRequestFactory

from transactions.serializers import CategorySerializer
from transactions.serializers import CategoryWriteSerializer


@pytest.mark.django_db
def test_serializer_create(category_recipe: str):
    """Test that the CategorySerializer reads the data correctly."""
    factory = APIRequestFactory()
    request = factory.get('/')
    category = baker.make_recipe(category_recipe)
    serializer = CategorySerializer(category, context={"request": request})
    assert serializer.data["id"] == str(category.id)
    assert serializer.data["name"] == category.name
    assert serializer.data["transaction_type"] is not None
    assert serializer.data["is_removed"] in [True, False]
    assert isinstance(serializer.data["transaction_type"], str)
    assert "/api/transaction_types/" in serializer.data["transaction_type"]


@pytest.mark.django_db
def test_write_serializer_create(category_recipe: str, transaction_type_recipe: str):
    """Test the CategoryWriteSerializer create method"""
    transaction_type = baker.make_recipe(transaction_type_recipe)
    user = transaction_type.user
    category = baker.prepare_recipe(
        category_recipe,
        transaction_type=transaction_type,
    )
    data = {
        "name": category.name,
        "transaction_type": transaction_type.pk,
    }
    mock_request = type("Request", (), {"user": user})()
    serializer = CategoryWriteSerializer(data=data, context={"request": mock_request})
    assert serializer.is_valid(), serializer.errors
    serialized_data = serializer.save()
    assert serialized_data.name == category.name
    assert serialized_data.transaction_type.pk == transaction_type.pk


@pytest.mark.django_db
def test_write_serializer_update(category_recipe: str, transaction_type_recipe: str):
    """Test the CategoryWriteSerializer update method"""
    transaction_type = baker.make_recipe(transaction_type_recipe)
    user = transaction_type.user
    category=baker.prepare_recipe(
        category_recipe,
        transaction_type=transaction_type,
    )
    data = {
        "transaction_type": category.transaction_type.pk,
        "name": f"{category.name}",
    }
    mock_request = type("Request", (), {"user": user})()
    serializer = CategoryWriteSerializer(category, data=data, context={"request": mock_request})
    assert serializer.is_valid(), serializer.errors
    updated_category = serializer.save()
    assert updated_category.name == data["name"]
    assert updated_category.transaction_type.pk == category.transaction_type.pk
