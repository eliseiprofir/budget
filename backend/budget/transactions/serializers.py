from rest_framework import serializers

from core.models import Bucket
from transactions.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model"""

    bucket = serializers.HyperlinkedRelatedField(
        view_name="api:bucket-detail",
        read_only=True,
    )

    class Meta:
        model = Category
        fields = ("id", "name", "bucket", "is_removed")
        read_only_fields = fields


class CategoryWriteSerializer(serializers.ModelSerializer):
    """Serializer used for create operations"""

    bucket = serializers.PrimaryKeyRelatedField(
        queryset=Bucket.available_objects.all(),
        required=True,
    )

    class Meta:
        model = Category
        fields = ("name", "bucket", "is_removed")
        read_only_fields = ("id",)
