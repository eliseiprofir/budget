from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserListSerializer
from core.models import Location
from core.models import Bucket
from core.serializers import LocationSerializer
from core.serializers import BucketSerializer
from transactions.models import TransactionType
from transactions.models import Category
from .models import Transaction


class TransactionTypeSerializer(serializers.ModelSerializer):
    """Serializer for the TransactionType model"""

    user = serializers.HyperlinkedRelatedField(
        view_name="api:user-detail",
        read_only=True,
    )

    class Meta:
        model = TransactionType
        fields = ("id", "name", "sign", "user", "is_removed")
        read_only_fields = fields


class TransactionTypeWriteSerializer(serializers.ModelSerializer):
    """Serializer used for create operations"""

    class Meta:
        model = TransactionType
        fields = ("name", "sign", "is_removed")
        read_only_fields = ("id", "user")

    def validate_name(self, value):
        user = self.context["request"].user
        if TransactionType.available_objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError(
                "You already have a bucket with that name."
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model"""

    transaction_type = serializers.HyperlinkedRelatedField(
        view_name="api:transaction_type-detail",
        read_only=True,
    )

    class Meta:
        model = Category
        fields = ("id", "name", "transaction_type", "is_removed")
        read_only_fields = fields


class CategoryWriteSerializer(serializers.ModelSerializer):
    """Serializer used for create operations"""

    transaction_type = serializers.PrimaryKeyRelatedField(
        queryset=TransactionType.available_objects.all(),
        required=True,
    )

    class Meta:
        model = Category
        fields = ("name", "transaction_type", "is_removed")
        read_only_fields = ("id",)

    def validate_name(self, value):
        transaction_type = self.initial_data.get("transaction_type")
        if Category.available_objects.filter(
                transaction_type=transaction_type, name=value
        ).exists():
            raise serializers.ValidationError(
                "You already have a category with that name."
            )
        return value


class TransactionListSerializer(serializers.ModelSerializer):
    """List Serializer for the Transaction model"""

    user = serializers.HyperlinkedRelatedField(
        view_name="api:user-detail",
        read_only=True,
    )
    category = serializers.HyperlinkedRelatedField(
        view_name="api:category-detail",
        read_only=True,
    )
    location = serializers.HyperlinkedRelatedField(
        view_name="api:location-detail",
        read_only=True,
    )
    bucket = serializers.HyperlinkedRelatedField(
        view_name="api:bucket-detail",
        read_only=True,
    )

    class Meta:
        model = Transaction
        fields = ("id", "user", "description", "transaction_type", "category", "date", "amount", "location", "bucket")
        read_only_fields = fields


class TransactionDetailSerializer(serializers.ModelSerializer):
    """Detail Serializer for the Transactions model"""

    user = UserListSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    bucket = BucketSerializer(read_only=True)

    class Meta(TransactionListSerializer.Meta):
        model = Transaction
        fields = (*TransactionListSerializer.Meta.fields, "user", "location", "bucket")
        read_only_fields = fields


class TransactionWriteSerializer(serializers.ModelSerializer):
    """Serializer used for create operations"""

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.available_objects.all(),
        required=True,
    )
    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.available_objects.all(),
        required=True,
    )
    bucket = serializers.PrimaryKeyRelatedField(
        queryset=Bucket.available_objects.all(),
        required=True,
    )

    class Meta:
        model = Transaction
        fields = ("description", "transaction_type", "category", "date", "amount", "location", "bucket")
        read_only_fields = ("id", "user")

    def validate(self, data):
        """Validate that bucket allocations are complete before allowing transaction creation."""

        user = self.context["request"].user
        if not Bucket.is_allocation_complete(user):
            raise serializers.ValidationError(
                "Cannot create transactions until bucket allocations total 100%. Please complete your bucket allocations first."
            )
        return data
