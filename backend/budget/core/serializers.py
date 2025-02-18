from decimal import Decimal

from rest_framework import serializers
from django.db import models
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

    def validate_name(self, name):
        """Validate location name is unique to current user."""

        user = self.context["request"].user
        current_query = Location.available_objects.filter(user=user, name=name)
        if self.instance:
            current_query = current_query.exclude(pk=self.instance.pk)
        if current_query.exists():
            raise serializers.ValidationError({"name": "You already have a location with this name."})
        return name


class BucketSerializer(serializers.ModelSerializer):
    """Serializer for the Bucket model"""

    user = serializers.HyperlinkedRelatedField(
        view_name="api:user-detail",
        read_only=True,
    )

    class Meta:
        model = Bucket
        fields = ("id", "name", "allocation_percentage", "allocation_status", "user", "is_removed")
        read_only_fields = fields


class BucketWriteSerializer(serializers.ModelSerializer):
    """Serializer used for create operations"""

    class Meta:
        model = Bucket
        fields = ("name", "allocation_percentage", "is_removed")
        read_only_fields = ("id", "user", "allocation_status")

    def validate_name(self, name):
        """Validate bucket name is unique to current user."""

        user = self.context["request"].user
        current_query = Bucket.available_objects.filter(user=user, name=name)
        if self.instance:
            current_query = current_query.exclude(pk=self.instance.pk)
        if current_query.exists():
            raise serializers.ValidationError({"name":"You already have a bucket with this name."})
        return name

    def validate_allocation_percentage(self, new_percentage):
        """Validate total allocation percentage does not exceed 100%."""

        if new_percentage < 0 or new_percentage > 100:
            raise serializers.ValidationError({"allocation_percentage":"Allocation percentage must be between 0 and 100."})
        user = self.context["request"].user
        current_total = Bucket.available_objects.filter(
            user=user
        ).aggregate(
            models.Sum("allocation_percentage")
        )["allocation_percentage__sum"] or Decimal("0")
        new_total = Decimal(str(current_total)) + Decimal(str(new_percentage))
        if new_total > 100:
            raise serializers.ValidationError({"allocation_percentage": f"Total allocation cannot exceed 100%. Allocation left: {100-current_total}%."})
        return new_percentage
