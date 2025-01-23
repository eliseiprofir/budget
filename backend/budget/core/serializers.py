from rest_framework import serializers

from core.models import Bucket
from core.models import Location

from accounts.models import User
from accounts.serializers import UserDetailSerializer

class BucketListSerializer(serializers.ModelSerializer):
    """List Serializer for the Bucket model"""

    user = serializers.HyperlinkedRelatedField(
        view_name="api:user-detail",
        read_only=True,
    )

    class Meta:
        model = Bucket
        fields = ("id", "name", "user", "allocation_percentage")
        read_only_fields = fields


class BucketDetailSerializer(serializers.ModelSerializer):
    """Detail Serializer for the Bucket model"""

    user = UserDetailSerializer(read_only=True)

    class Meta(BucketListSerializer.Meta):
        fields = (*BucketListSerializer.Meta.fields, "is_removed")
        read_only_fields = fields


class BucketWriteSerializer(serializers.ModelSerializer):
    """Serializer used for create operations"""

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
    )

    class Meta:
        model = Bucket
        fields = ("name", "user", "allocation_percentage")
        read_only_fields = ("id",)


class LocationListSerializer(serializers.ModelSerializer):
    """List Serializer for the Location model"""

    user = serializers.HyperlinkedRelatedField(
        view_name="api:user-detail",
        read_only=True,
    )

    class Meta:
        model = Location
        fields = ("id", "name", "user")
        read_only_fields = fields


class LocationDetailSerializer(serializers.ModelSerializer):
    """Detail Serializer for the Location model"""

    user = UserDetailSerializer(read_only=True)

    class Meta(LocationListSerializer.Meta):
        fields = (*LocationListSerializer.Meta.fields, "is_removed")
        read_only_fields = fields


class LocationWriteSerializer(serializers.ModelSerializer):
    """Serializer used for create operations"""

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
    )

    class Meta:
        model = Location
        fields = ("name", "user")
        read_only_fields = ("id",)
