import pytest
from model_bakery import baker
from rest_framework.test import APIRequestFactory

from core.serializers import BucketSerializer
from core.serializers import BucketWriteSerializer


@pytest.mark.django_db
def test_serializer_create(bucket_recipe: str):
    """Test that the BucketSerializer reads the data correctly."""
    factory = APIRequestFactory()
    request = factory.get('/')
    bucket = baker.make_recipe(bucket_recipe)
    serializer = BucketSerializer(bucket, context={"request": request})
    assert serializer.data["id"] == str(bucket.id)
    assert serializer.data["name"] == bucket.name
    assert serializer.data["allocation_percentage"] is not None
    assert serializer.data["allocation_status"] != ""
    assert serializer.data["user"] is not None
    assert serializer.data["is_removed"] in [True, False]
    assert isinstance(serializer.data["user"], str)
    assert "/api/users/" in serializer.data["user"]


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
    }
    mock_request = type("Request", (), {"user": user})()
    serializer = BucketWriteSerializer(data=data, context={"request": mock_request})
    assert serializer.is_valid(), serializer.errors
    serialized_data = serializer.save(user=user)
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
    mock_request = type("Request", (), {"user": user})()
    serializer = BucketWriteSerializer(bucket, data=data, context={"request": mock_request})
    assert serializer.is_valid(), serializer.errors
    updated_bucket = serializer.save()
    assert updated_bucket.name == data["name"]
    assert str(updated_bucket.allocation_percentage) == data["allocation_percentage"]
    assert updated_bucket.user.pk == bucket.user.pk
