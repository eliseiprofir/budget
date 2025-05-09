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
    assert serializer.data["sign"] == category.sign
    assert serializer.data["is_removed"] in [True, False]
    assert serializer.data["user"] is not None
    assert "/api/users/" in serializer.data["user"]
    assert isinstance(serializer.data["user"], str)


@pytest.mark.django_db
def test_write_serializer_create(category_recipe: str, user_recipe: str):
    """Test the CategoryWriteSerializer create method"""
    user = baker.make_recipe(user_recipe)
    category = baker.prepare_recipe(
        category_recipe,
        user=user,
    )
    data = {
        "name": category.name,
        "sign": category.sign,
        "user": category.user.pk,
    }
    mock_request = type("Request", (), {"user": user})()
    serializer = CategoryWriteSerializer(data=data, context={"request": mock_request})
    assert serializer.is_valid(), serializer.errors
    serialized_data = serializer.save(user=user)
    assert serialized_data.name == category.name
    assert serialized_data.sign == category.sign
    assert serialized_data.user.pk == user.pk


@pytest.mark.django_db
def test_write_serializer_update(category_recipe: str, user_recipe: str):
    """Test the CategoryWriteSerializer update method"""
    user = baker.make_recipe(user_recipe)
    category=baker.prepare_recipe(
        category_recipe,
        user=user,
    )
    data = {
        "name": f"{category.name}",
        "sign": f"{category.sign}",
        "user": category.user.pk,
    }
    mock_request = type("Request", (), {"user": user})()
    serializer = CategoryWriteSerializer(category, data=data, context={"request": mock_request})
    assert serializer.is_valid(), serializer.errors
    updated_category = serializer.save()
    assert updated_category.name == data["name"]
    assert updated_category.sign == data["sign"]
    assert updated_category.user.pk == category.user.pk
