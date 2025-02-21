import pytest
from model_bakery import baker
from django.core.exceptions import ValidationError
from core.models import Bucket


@pytest.mark.django_db
def test_bucket_creation(bucket_recipe: str):
    """Test creating a Bucket instance with valid data"""
    bucket = baker.make_recipe(bucket_recipe)
    assert bucket.pk is not None
    assert bucket.name != ""
    assert bucket.allocation_percentage != ""
    assert bucket.allocation_status != ""
    assert bucket.is_removed in [True, False]
    assert bucket.user.pk != ""


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
def test_get_total_allocation_percentage(user_recipe: str, bucket_recipe: str):
    """Test getting total allocation percentage"""
    user1 = baker.make_recipe(user_recipe)
    user2 = baker.make_recipe(user_recipe)
    user1_bucket1 = baker.make_recipe(bucket_recipe, user=user1, allocation_percentage=50)
    user1_bucket2 = baker.make_recipe(bucket_recipe, user=user1, allocation_percentage=50)
    user2_bucket1 = baker.make_recipe(bucket_recipe, user=user2, allocation_percentage=30)
    assert user1_bucket1.get_total_allocation_percentage() == 100.0
    assert user1_bucket2.get_total_allocation_percentage() == 100.0
    assert user2_bucket1.get_total_allocation_percentage() == 30.0


@pytest.mark.django_db
def test_get_available_percentage(user_recipe: str, bucket_recipe: str):
    """Test getting total allocation percentage"""
    user1 = baker.make_recipe(user_recipe)
    user2 = baker.make_recipe(user_recipe)
    user1_bucket1 = baker.make_recipe(bucket_recipe, user=user1, allocation_percentage=50)
    user1_bucket2 = baker.make_recipe(bucket_recipe, user=user1, allocation_percentage=50)
    user2_bucket1 = baker.make_recipe(bucket_recipe, user=user2, allocation_percentage=30)
    assert user1_bucket1.get_available_percentage() == 0.0
    assert user1_bucket2.get_available_percentage() == 0.0
    assert user2_bucket1.get_available_percentage() == 70.0


@pytest.mark.django_db
def test_is_allocation_complete(user_recipe: str, bucket_recipe: str):
    """Test getting total allocation percentage"""
    user1 = baker.make_recipe(user_recipe)
    user2 = baker.make_recipe(user_recipe)
    user1_bucket1 = baker.make_recipe(bucket_recipe, user=user1, allocation_percentage=50)
    user1_bucket2 = baker.make_recipe(bucket_recipe, user=user1, allocation_percentage=50)
    user2_bucket1 = baker.make_recipe(bucket_recipe, user=user2, allocation_percentage=30)
    assert user1_bucket1.is_allocation_complete(user1) is True
    assert user1_bucket2.is_allocation_complete(user1) is True
    assert user2_bucket1.is_allocation_complete(user2) is False


@pytest.mark.django_db
def test_validate_name(user_recipe: str, bucket_recipe: str):
    """Test validating the name field"""
    user = baker.make_recipe(user_recipe)
    bucket = baker.make_recipe(bucket_recipe, user=user)
    with pytest.raises(ValidationError):
        baker.make_recipe(bucket_recipe, name=bucket.name, user=user)


@pytest.mark.django_db
def test_validate_allocation_percentage(user_recipe: str, bucket_recipe: str):
    """Test validating the allocation_percentage field"""
    with pytest.raises(ValidationError):
        baker.make_recipe(bucket_recipe, allocation_percentage=-5)
    with pytest.raises(ValidationError):
        baker.make_recipe(bucket_recipe, allocation_percentage=105)

    user = baker.make_recipe(user_recipe)
    baker.make_recipe(bucket_recipe, user=user, allocation_percentage=50)
    with pytest.raises(ValidationError):
        baker.make_recipe(bucket_recipe, allocation_percentage=60, user=user)


@pytest.mark.django_db
def test_allocation_status(user_recipe: str, bucket_recipe: str):
    """Test allocation status change accordingly."""
    user = baker.make_recipe(user_recipe)
    bucket1 = baker.make_recipe(bucket_recipe, user=user, allocation_percentage=50)
    assert bucket1.allocation_status == Bucket.AllocationStatus.INCOMPLETE
    bucket2 = baker.make_recipe(bucket_recipe, user=user, allocation_percentage=50)
    bucket1.refresh_from_db()
    bucket2.refresh_from_db()
    assert bucket1.allocation_status == Bucket.AllocationStatus.COMPLETE
    assert bucket2.allocation_status == Bucket.AllocationStatus.COMPLETE
    bucket1.allocation_percentage = 49
    bucket1.save()
    bucket1.refresh_from_db()
    bucket2.refresh_from_db()
    assert bucket1.allocation_status == Bucket.AllocationStatus.INCOMPLETE
    assert bucket2.allocation_status == Bucket.AllocationStatus.INCOMPLETE


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
