from rest_framework import serializers

from core.models import Bucket
from accounts.models import User
from transactions.models import Entry
from transactions.models import Category


class EntrySerializer(serializers.ModelSerializer):
    """Serializer for the Entry model"""

    class Meta:
        model = Entry
        fields = ("id", "name",)
        read_only_fields = fields


class EntryWriteSerializer(serializers.ModelSerializer):
    """Serializer used for create operations"""

    class Meta:
        model = Entry
        fields = ("name",)
        read_only_fields = ("id",)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model"""

    bucket = serializers.HyperlinkedRelatedField(
        view_name="api:bucket-detail",
        read_only=True,
    )
    user = serializers.HyperlinkedRelatedField(
        view_name="api:user-detail",
        read_only=True,
    )

    class Meta:
        model = Category
        fields = ("id", "name", "bucket", "user", "is_removed")
        read_only_fields = fields


class CategoryWriteSerializer(serializers.ModelSerializer):
    """Serializer used for create operations"""

    bucket = serializers.PrimaryKeyRelatedField(
        queryset=Bucket.available_objects.all(),
        required=True,
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
    )

    class Meta:
        model = Category
        fields = ("name", "bucket", "user", "is_removed")
        read_only_fields = ("id",)
