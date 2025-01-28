import pytest
from model_bakery import baker
from rest_framework.test import APIRequestFactory

from transactions.serializers import CategorySerializer
from transactions.serializers import CategoryWriteSerializer


@pytest.mark.django_db
def test_serializer_create(category_recipe: str):
    """Test that the CategorySerializer reads the data correctly."""
    factory = APIRequestFactory()
    request = factory.get('/')
    category = baker.make_recipe(category_recipe)
    serializer = CategorySerializer(category, context={"request": request})
    assert serializer.data["id"] == str(category.id)
    assert serializer.data["name"] == category.name
    assert serializer.data["bucket"] is not None
    assert serializer.data["is_removed"] in [True, False]
    assert isinstance(serializer.data["bucket"], str)
    assert "/api/buckets/" in serializer.data["bucket"]


@pytest.mark.django_db
def test_write_serializer_create(category_recipe: str, bucket_recipe: str):
    """Test the CategoryWriteSerializer create method"""
    bucket = baker.make_recipe(bucket_recipe)
    category = baker.prepare_recipe(
        category_recipe,
        bucket=bucket,
    )
    data = {
        "name": category.name,
        "bucket": bucket.pk,
    }
    serializer = CategoryWriteSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    serialized_data = serializer.save()
    assert serialized_data.name == category.name
    assert serialized_data.bucket.pk == bucket.pk


@pytest.mark.django_db
def test_write_serializer_update(category_recipe: str, bucket_recipe: str):
    """Test the CategoryWriteSerializer update method"""
    bucket = baker.make_recipe(bucket_recipe)
    category=baker.prepare_recipe(
        category_recipe,
        bucket=bucket,
    )
    data = {
        "bucket": category.bucket.pk,
        "name": f"{category.name}",
    }
    serializer = CategoryWriteSerializer(category, data=data)
    assert serializer.is_valid(), serializer.errors
    updated_category = serializer.save()
    assert updated_category.name == data["name"]
    assert updated_category.bucket.pk == category.bucket.pk
