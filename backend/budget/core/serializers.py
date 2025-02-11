from rest_framework import serializers

from core.models import Bucket
from core.models import Location


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

    class Meta:
        model = Location
        fields = ("name", "is_removed")
        read_only_fields = ("id", "user")

    def validate_name(self, value):
        user = self.context["request"].user
        if Location.available_objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError(
                "You already have a location with that name."
            )
        return value



class BucketSerializer(serializers.ModelSerializer):
    """Serializer for the Bucket model"""

    user = serializers.HyperlinkedRelatedField(
        view_name="api:user-detail",
        read_only=True,
    )

    class Meta:
        model = Bucket
        fields = ("id", "name", "allocation_percentage", "user", "is_removed")
        read_only_fields = fields


class BucketWriteSerializer(serializers.ModelSerializer):
    """Serializer used for create operations"""

    class Meta:
        model = Bucket
        fields = ("name", "allocation_percentage", "is_removed")
        read_only_fields = ("id", "user")

    def validate_name(self, value):
        user = self.context["request"].user
        if Bucket.available_objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError(
                "You already have a bucket with that name."
            )
        return value
