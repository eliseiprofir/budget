import pytest
from model_bakery import baker
from transactions.models import Category


@pytest.mark.django_db
def test_category_creation(category_recipe: str):
    """Test creating a Category instance with valid data"""
    category = baker.make_recipe(category_recipe)
    assert category.pk is not None
    assert category.name != ""
    assert category.bucket != ""
    assert category.is_removed in [True, False]


@pytest.mark.django_db
def test_crud_operations(category_recipe: str):
    """Test the CRUD operations for the model"""

    # Create
    name = "Clothes"
    category = baker.make_recipe(
        category_recipe,
        name=name,
    )
    assert Category.available_objects.count() == 1
    assert category.name == name

    # Read
    fetched_category = Category.available_objects.get(pk=category.pk)
    assert fetched_category.name == name

    # Update
    category.name = "Books"
    category.save()
    updated_category = Category.available_objects.get(pk=category.pk)
    assert updated_category.name == "Books"

    # Delete
    category.delete()
    assert Category.available_objects.count() == 0


@pytest.mark.django_db
def test_str_method(category: Category):
    """Test the string representation of the model"""
    assert str(category) == f"{category.name}"


@pytest.mark.django_db
def test_meta_class(category_recipe: str):
    """Test the meta options"""
    category = baker.prepare_recipe(category_recipe)
    assert category._meta.verbose_name == "Category"
    assert category._meta.verbose_name_plural == "Categories"
    assert category._meta.ordering == ("name",)
