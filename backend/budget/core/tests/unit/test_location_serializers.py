import pytest
from model_bakery import baker

from core.serializers import LocationSerializer
from core.serializers import LocationWriteSerializer


@pytest.mark.django_db
def test_serializer_create(location_recipe: str):
    """Test that the LocationSerializer reads the data correctly."""
    location = baker.make_recipe(location_recipe)
    serializer = LocationSerializer(location)
    assert serializer.data["id"] == str(location.id)
    assert serializer.data["name"] == location.name
    assert serializer.data["user"] is not None
    assert serializer.data["is_removed"] in [True, False]


@pytest.mark.django_db
def test_write_serializer_create(location_recipe: str, user_recipe: str):
    """Test the LocationWriteSerializer create method"""
    user = baker.make_recipe(user_recipe)
    location = baker.prepare_recipe(
        location_recipe,
        user=user,
    )
    data = {
        "name": location.name,
        "user": user.pk,
    }
    serializer = LocationWriteSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    serialized_data = serializer.save()
    assert serialized_data.name == location.name
    assert serialized_data.user.pk == user.pk


@pytest.mark.django_db
def test_write_serializer_update(location_recipe: str, user_recipe: str):
    """Test the LocationWriteSerializer update method"""
    user = baker.make_recipe(user_recipe)
    location=baker.prepare_recipe(
        location_recipe,
        user=user,
    )
    data = {
        "user": location.user.pk,
        "name": f"{location.name}",
    }
    serializer = LocationWriteSerializer(location, data=data)
    assert serializer.is_valid(), serializer.errors
    updated_location = serializer.save()
    assert updated_location.name == data["name"]
    assert updated_location.user.pk == location.user.pk
