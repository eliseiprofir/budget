import pytest
from model_bakery import baker

from transactions.serializers import EntrySerializer
from transactions.serializers import EntryWriteSerializer


@pytest.mark.django_db
def test_serializer_create(entry_recipe: str):
    """Test that the EntrySerializer reads the data correctly."""
    entry = baker.make_recipe(entry_recipe)
    serializer = EntrySerializer(entry)
    assert serializer.data["id"] == str(entry.id)
    assert serializer.data["name"] == entry.name


@pytest.mark.django_db
def test_write_serializer_create(entry_recipe: str):
    """Test the EntryWriteSerializer create method"""
    entry = baker.prepare_recipe(entry_recipe)
    data = {"name": entry.name}
    serializer = EntryWriteSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    serialized_data = serializer.save()
    assert serialized_data.name == entry.name


@pytest.mark.django_db
def test_write_serializer_update(entry_recipe: str):
    """Test the EntryWriteSerializer update method"""
    entry=baker.prepare_recipe(entry_recipe)
    data = {"name": f"{entry.name}"}
    serializer = EntryWriteSerializer(entry, data=data)
    assert serializer.is_valid(), serializer.errors
    updated_entry = serializer.save()
    assert updated_entry.name == data["name"]
