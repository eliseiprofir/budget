import pytest
from model_bakery import baker

from accounts.serializers import UserDetailSerializer
from accounts.serializers import UserWriteSerializer


@pytest.mark.django_db
def test_detail_serializer_create(user_recipe: str):
    """Test that the UserDetailSerializer reads the data correctly."""
    user = baker.make_recipe(user_recipe)
    serializer = UserDetailSerializer(user)
    assert serializer.data["id"] == str(user.id)
    assert serializer.data["email"] == user.email
    assert serializer.data["last_login"] is None
    assert serializer.data["created"] is not None
    assert serializer.data["modified"] is not None
    assert serializer.data["is_active"] in [True, False]


@pytest.mark.django_db
def test_write_serializer_create(user_recipe: str):
    """Test the UserWriteSerializer create method"""
    user = baker.prepare_recipe(user_recipe)
    data = {
        "full_name": user.full_name,
        "email": user.email,
    }
    serializer = UserWriteSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    serialized_data = serializer.save()
    assert serialized_data.full_name == user.full_name
    assert serialized_data.email == user.email


@pytest.mark.django_db
def test_write_serializer_update(user_recipe: str):
    """Test the UserWriteSerializer update method"""
    user = baker.make_recipe(user_recipe)
    data = {
        "full_name": f"{user.full_name} - unique",
        "email": "updated@email.com",
    }
    serializer = UserWriteSerializer(user, data=data)
    assert serializer.is_valid(), serializer.errors
    updated_user = serializer.save()
    assert updated_user.full_name == data["full_name"]
    assert updated_user.email == data["email"]
