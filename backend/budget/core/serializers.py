from rest_framework import serializers

from core.models import Bucket
from core.models import Location

from accounts.models import User


class LocationSerializer(serializers.ModelSerializer):
    """Detail Serializer for the Location model"""

    user = serializers.HyperlinkedRelatedField(
        view_name="api:user-detail",
        read_only=True,
    )

    class Meta:
        model = Location
        fields = ("id", "name", "user", "is_removed")
        read_only_fields = fields


class LocationWriteSerializer(serializers.ModelSerializer):
    """Serializer used for create operations"""

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
    )

    class Meta:
        model = Location
        fields = ("name", "user", "is_removed")
        read_only_fields = ("id",)


class BucketSerializer(serializers.ModelSerializer):
    """Serializer for the Bucket model"""

    user = serializers.HyperlinkedRelatedField(
        view_name="api:user-detail",
        read_only=True,
    )

    class Meta:
        model = Bucket
        fields = ("id", "name", "user", "allocation_percentage", "is_removed")
        read_only_fields = fields


class BucketWriteSerializer(serializers.ModelSerializer):
    """Serializer used for create operations"""

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
    )

    class Meta:
        model = Bucket
        fields = ("name", "user", "allocation_percentage", "is_removed")
        read_only_fields = ("id",)
