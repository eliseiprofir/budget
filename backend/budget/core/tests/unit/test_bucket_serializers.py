import pytest
from model_bakery import baker

from core.serializers import BucketDetailSerializer
from core.serializers import BucketWriteSerializer


@pytest.mark.django_db
def test_detail_serializer_create(bucket_recipe: str):
    """Test that the BucketDetailSerializer reads the data correctly."""
    bucket = baker.make_recipe(bucket_recipe)
    serializer = BucketDetailSerializer(bucket)
    assert serializer.data["id"] == str(bucket.id)
    assert serializer.data["name"] == bucket.name
    assert serializer.data["allocation_percentage"] is not None
    assert serializer.data["user"] is not None
    assert serializer.data["is_removed"] in [True, False]


@pytest.mark.django_db
def test_write_serializer_create(bucket_recipe: str, user_recipe: str):
    """Test the BucketWriteSerializer create method"""
    user = baker.make_recipe(user_recipe)
    bucket = baker.prepare_recipe(
        bucket_recipe,
        user=user,
    )
    data = {
        "name": bucket.name,
        "allocation_percentage": bucket.allocation_percentage,
        "user": user.pk,
    }
    serializer = BucketWriteSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    serialized_data = serializer.save()
    assert serialized_data.name == bucket.name
    assert serialized_data.allocation_percentage == bucket.allocation_percentage
    assert serialized_data.user.pk == user.pk


@pytest.mark.django_db
def test_write_serializer_update(bucket_recipe: str, user_recipe: str):
    """Test the BucketWriteSerializer update method"""
    user = baker.make_recipe(user_recipe)
    bucket=baker.prepare_recipe(
        bucket_recipe,
        user=user,
    )
    data = {
        "user": bucket.user.pk,
        "name": f"{bucket.name}",
        "allocation_percentage": "55.55",
    }
    serializer = BucketWriteSerializer(bucket, data=data)
    assert serializer.is_valid(), serializer.errors
    updated_bucket = serializer.save()
    assert updated_bucket.name == data["name"]
    assert str(updated_bucket.allocation_percentage) == data["allocation_percentage"]
    assert updated_bucket.user.pk == bucket.user.pk
