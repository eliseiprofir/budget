import pytest
from model_bakery import baker
from django.core.exceptions import ValidationError
from accounts.models import User


@pytest.mark.django_db
def test_user_creation(user_recipe: str):
    """Test creating a User instance with valid data"""
    user = baker.make_recipe(user_recipe)
    assert user.pk is not None
    assert user.full_name != ""
    assert user.email != ""
    assert user.last_login != ""


@pytest.mark.django_db
def test_is_active_validation(user_recipe: str):
    """Test validation for is_active field"""
    user = baker.prepare_recipe(
        user_recipe,
        is_active=None,
    )
    with pytest.raises(ValidationError):
        user.full_clean()


@pytest.mark.django_db
def test_crud_operations(user_recipe: str):
    """Test the CRUD operations for the model"""

    # Create
    full_name = "Andrei Popa"
    user = baker.make_recipe(
        user_recipe,
        full_name=full_name,
    )
    assert User.available_objects.count() == 1
    assert user.full_name == full_name

    # Read
    fetched_user = User.available_objects.get(pk=user.pk)
    assert fetched_user.full_name == full_name

    # Update
    user.full_name = "Vasile Paul"
    user.save()
    updated_user = User.available_objects.get(pk=user.pk)
    assert updated_user.full_name == "Vasile Paul"

    # Delete
    user.delete()
    assert User.available_objects.count() == 0


@pytest.mark.django_db
def test_str_method(user: User):
    """Test the string representation of the model"""
    assert str(user) == f"{user.full_name} ({user.email})"


@pytest.mark.django_db
def test_meta_class(user_recipe: str):
    """Test the meta options"""
    user = baker.prepare_recipe(user_recipe)
    assert user._meta.verbose_name == "User"
    assert user._meta.verbose_name_plural == "Users"
    assert user._meta.ordering == ("-created",)
