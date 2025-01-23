import pytest
from model_bakery import baker
from core.models import Bucket


@pytest.mark.django_db
def test_bucket_creation(bucket_recipe: str):
    """Test creating a Bucket instance with valid data"""
    bucket = baker.make_recipe(bucket_recipe)
    assert bucket.pk is not None
    assert bucket.name != ""
    assert bucket.user != ""
    assert bucket.is_removed in [True, False]


@pytest.mark.django_db
def test_crud_operations(bucket_recipe: str):
    """Test the CRUD operations for the model"""

    # Create
    name = "Donation"
    bucket = baker.make_recipe(
        bucket_recipe,
        name=name,
    )
    assert Bucket.available_objects.count() == 1
    assert bucket.name == name

    # Read
    fetched_bucket = Bucket.available_objects.get(pk=bucket.pk)
    assert fetched_bucket.name == name

    # Update
    bucket.name = "Economy"
    bucket.save()
    updated_bucket = Bucket.available_objects.get(pk=bucket.pk)
    assert updated_bucket.name == "Economy"

    # Delete
    bucket.delete()
    assert Bucket.available_objects.count() == 0

@pytest.mark.django_db
def test_str_method(bucket: Bucket):
    """Test the string representation of the model"""
    assert str(bucket) == f"{bucket.name}"

@pytest.mark.django_db
def test_meta_class(bucket_recipe: str):
    """Test the meta options"""
    bucket = baker.prepare_recipe(bucket_recipe)
    assert bucket._meta.verbose_name == "Bucket"
    assert bucket._meta.verbose_name_plural == "Buckets"
    assert bucket._meta.ordering == ("name",)
