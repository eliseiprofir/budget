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

    class Meta:
        model = TransactionType
        fields = ("id", "name", "is_removed")
        read_only_fields = fields


class TransactionTypeWriteSerializer(serializers.ModelSerializer):
    """Serializer used for create operations"""

    class Meta:
        model = TransactionType
        fields = ("name", "is_removed")
        read_only_fields = ("id",)


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

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.available_objects.all(),
        required=True,
    )
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
        fields = ("user", "description", "transaction_type", "category", "date", "amount", "location", "bucket")
        read_only_fields = ("id",)
