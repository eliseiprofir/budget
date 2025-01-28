import pytest
from model_bakery import baker
from transactions.models import Entry


@pytest.mark.django_db
def test_entry_creation(entry_recipe: str):
    """Test creating an Entry instance with valid data"""
    entry = baker.make_recipe(entry_recipe)
    assert entry.pk is not None
    assert entry.name != ""

@pytest.mark.django_db
def test_entry_unique_validation(entry: Entry, entry_recipe: str):
    """Test validation for name field - should be unique"""
    entry2 = baker.prepare_recipe(
        entry_recipe,
        name=entry.name,
    )
    with pytest.raises(ValidationError):
        entry2.full_clean()

@pytest.mark.django_db
def test_crud_operations(entry_recipe: str):
    """Test the CRUD operations for the model"""

    # Create
    name = Entry.Name.EXPENSE
    entry = baker.make_recipe(
        entry_recipe,
        name=name,
    )
    assert Entry.objects.count() == 1
    assert entry.name == name

    # Read
    fetched_entry = Entry.objects.get(pk=entry.pk)
    assert fetched_entry.name == name

    # Update
    entry.name = Entry.Name.INCOME
    entry.save()
    updated_entry = Entry.objects.get(pk=entry.pk)
    assert updated_entry.name == Entry.Name.INCOME

    # Delete
    entry.delete()
    assert Entry.objects.count() == 0

@pytest.mark.django_db
def test_str_method(entry: Entry):
    """Test the string representation of the model"""
    assert str(entry) == f"{entry.name}"

@pytest.mark.django_db
def test_meta_class(entry_recipe: str):
    """Test the meta options"""
    entry = baker.prepare_recipe(entry_recipe)
    assert entry._meta.verbose_name == "Entry"
    assert entry._meta.verbose_name_plural == "Entries"
    assert entry._meta.ordering == ("name",)
