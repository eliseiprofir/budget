import pytest
from model_bakery import baker
from rest_framework.test import APIRequestFactory

from transactions.serializers import TransactionTypeSerializer
from transactions.serializers import TransactionTypeWriteSerializer


@pytest.mark.django_db
def test_serializer_create(transaction_type_recipe: str):
    """Test that the TransactionTypeSerializer reads the data correctly."""
    factory = APIRequestFactory()
    request = factory.get('/')
    transaction_type = baker.make_recipe(transaction_type_recipe)
    serializer = TransactionTypeSerializer(transaction_type, context={"request": request})
    assert serializer.data["id"] == str(transaction_type.id)
    assert serializer.data["sign"] == transaction_type.sign
    assert serializer.data["name"] == transaction_type.name
    assert serializer.data["is_removed"] in [True, False]


@pytest.mark.django_db
def test_write_serializer_create(transaction_type_recipe: str):
    """Test the TransactionTypeWriteSerializer create method"""
    transaction_type = baker.prepare_recipe(transaction_type_recipe)
    data = {
        "sign": transaction_type.sign,
        "name": transaction_type.name,
    }
    serializer = TransactionTypeWriteSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    serialized_data = serializer.save()
    assert serialized_data.sign == transaction_type.sign
    assert serialized_data.name == transaction_type.name


@pytest.mark.django_db
def test_write_serializer_update(transaction_type_recipe: str):
    """Test the TransactionTypeWriteSerializer update method"""
    transaction_type=baker.prepare_recipe(
        transaction_type_recipe,
    )
    data = {
        "sign": f"{transaction_type.sign}",
        "name": f"{transaction_type.name}",
    }
    serializer = TransactionTypeWriteSerializer(transaction_type, data=data)
    assert serializer.is_valid(), serializer.errors
    updated_transaction_type = serializer.save()
    assert updated_transaction_type.sign == data["sign"]
    assert updated_transaction_type.name == data["name"]
