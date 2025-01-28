import pytest
from model_bakery import baker
from core.models import Location


@pytest.mark.django_db
def test_location_creation(location_recipe: str):
    """Test creating a Location instance with valid data"""
    location = baker.make_recipe(location_recipe)
    assert location.pk is not None
    assert location.name != ""
    assert location.user != ""
    assert location.is_removed in [True, False]


@pytest.mark.django_db
def test_crud_operations(location_recipe: str):
    """Test the CRUD operations for the model"""

    # Create
    name = "Card"
    location = baker.make_recipe(
        location_recipe,
        name=name,
    )
    assert Location.available_objects.count() == 1
    assert location.name == name

    # Read
    fetched_location = Location.available_objects.get(pk=location.pk)
    assert fetched_location.name == name

    # Update
    location.name = "Cash"
    location.save()
    updated_location = Location.available_objects.get(pk=location.pk)
    assert updated_location.name == "Cash"

    # Delete
    location.delete()
    assert Location.available_objects.count() == 0


@pytest.mark.django_db
def test_str_method(location: Location):
    """Test the string representation of the model"""
    assert str(location) == f"{location.name}"


@pytest.mark.django_db
def test_meta_class(location_recipe: str):
    """Test the meta options"""
    location = baker.prepare_recipe(location_recipe)
    assert location._meta.verbose_name == "Location"
    assert location._meta.verbose_name_plural == "Locations"
    assert location._meta.ordering == ("name",)
