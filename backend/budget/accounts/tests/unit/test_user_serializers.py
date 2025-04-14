import pytest
from model_bakery import baker

from accounts.serializers import UserListSerializer
from accounts.serializers import UserDetailSerializer
from accounts.serializers import UserCreateSerializer
from accounts.serializers import UserUpdateSerializer


@pytest.mark.django_db
def test_list_serializer_create(user_recipe: str):
    """Test that the UserListSerializer reads the data correctly."""
    user = baker.make_recipe(user_recipe)
    serializer = UserListSerializer(user)
    assert serializer.data["id"] == str(user.id)
    assert serializer.data["email"] == user.email
    assert serializer.data["full_name"] == user.full_name
    assert serializer.data["is_active"] == user.is_active


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
def test_create_serializer_create(user_recipe: str):
    """Test the UserCreateSerializer create method"""
    user = baker.prepare_recipe(user_recipe)
    data = {
        "full_name": user.full_name,
        "email": user.email,
        "password": "testpassword123"
    }
    serializer = UserCreateSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    serialized_data = serializer.save()
    assert serialized_data.full_name == user.full_name
    assert serialized_data.email == user.email
    assert serialized_data.check_password("testpassword123")


@pytest.mark.django_db
def test_update_serializer_update(user_recipe: str):
    """Test the UserUpdateSerializer update method"""
    user = baker.make_recipe(user_recipe)
    data = {
        "full_name": f"{user.full_name} - unique",
        "email": "updated@email.com",
        "password": "newpassword123"
    }
    serializer = UserUpdateSerializer(user, data=data)
    assert serializer.is_valid(), serializer.errors
    updated_user = serializer.save()
    assert updated_user.full_name == data["full_name"]
    assert updated_user.email == data["email"]
    assert updated_user.check_password("newpassword123")


@pytest.mark.django_db
def test_update_serializer_update_without_password(user_recipe: str):
    """Test the UserUpdateSerializer update method without changing password"""
    user = baker.make_recipe(user_recipe)
    original_password_hash = user.password
    data = {
        "full_name": f"{user.full_name} - unique",
        "email": "updated@email.com",
    }
    serializer = UserUpdateSerializer(user, data=data)
    assert serializer.is_valid(), serializer.errors
    updated_user = serializer.save()
    assert updated_user.full_name == data["full_name"]
    assert updated_user.email == data["email"]
    assert updated_user.password == original_password_hash
