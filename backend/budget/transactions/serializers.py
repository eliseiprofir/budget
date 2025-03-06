from rest_framework import serializers

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
        fields = ("id", "name", "sign", "is_removed", "user")
        read_only_fields = fields

    def validate_name(self, name):
        """Validate transaction type name is unique to current user."""
        user = self.context["request"].user
        current_query = TransactionType.available_objects.filter(user=user, name=name)
        if self.instance:
            current_query = current_query.exclude(pk=self.instance.pk)
        if current_query.exists():
            raise serializers.ValidationError({"name": "You already have a transaction type with this name."})
        return name


class TransactionTypeWriteSerializer(serializers.ModelSerializer):
    """Serializer used for create operations"""

    class Meta:
        model = TransactionType
        fields = ("name", "sign", "is_removed")
        read_only_fields = ("id", "user")

    def validate_name(self, value):
        user = self.context["request"].user
        if TransactionType.available_objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError({"name": "You already have a bucket with that name."})
        return value


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model"""
    transaction_type = serializers.HyperlinkedRelatedField(
        view_name="api:transaction-type-detail",
        read_only=True,
    )
    user = serializers.HyperlinkedRelatedField(
        view_name="api:user-detail",
        read_only=True,
    )

    class Meta:
        model = Category
        fields = ("id", "name", "transaction_type", "is_removed", "user")
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
        read_only_fields = ("id", "user")

    def __init__(self, *args, **kwargs):
        """Override get_queryset to filter transaction types by user."""
        super().__init__(*args, **kwargs)

        if "request" in self.context:
            user = self.context["request"].user
            filtered_queryset = self.fields["transaction_type"].queryset.filter_by_user(user)
            self.fields["transaction_type"].queryset = filtered_queryset

    def validate_name(self, value):
        user = self.context["request"].user
        if Category.available_objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError({"name": "You already have a category with that name."})
        return value


class TransactionListSerializer(serializers.ModelSerializer):
    """List Serializer for the Transaction model"""
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
    user = serializers.HyperlinkedRelatedField(
        view_name="api:user-detail",
        read_only=True,
    )

    class Meta:
        model = Transaction
        fields = ("id", "description", "transaction_type", "category", "date", "amount", "location", "bucket", "split_income", "user")
        read_only_fields = fields


class TransactionDetailSerializer(serializers.ModelSerializer):
    """Detail Serializer for the Transactions model"""
    user = UserListSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    bucket = BucketSerializer(read_only=True)

    class Meta(TransactionListSerializer.Meta):
        model = Transaction
        fields = (*TransactionListSerializer.Meta.fields, "parent_transaction")
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
        fields = ("description", "transaction_type", "category", "date", "amount", "location", "bucket", "split_income",)
        read_only_fields = ("id", "parent_transaction", "user")

    def __init__(self, *args, **kwargs):
        """Override get_queryset to filter transaction categories, locations and buckets by user."""
        super().__init__(*args, **kwargs)

        if "request" in self.context:
            user = self.context["request"].user

            category_filtered_queryset = self.fields["category"].queryset.filter_by_user(user)
            self.fields["category"].queryset = category_filtered_queryset

            location_filtered_queryset = self.fields["location"].queryset.filter_by_user(user)
            self.fields["location"].queryset = location_filtered_queryset

            bucket_filtered_queryset = self.fields["bucket"].queryset.filter_by_user(user)
            self.fields["bucket"].queryset = bucket_filtered_queryset

    def validate(self, data):
        """Validate transaction data."""
        user = self.context["request"].user
        category = data["category"]
        split_income = data.get("split_income")
        bucket = data["bucket"]

        errors = {}

        # Validate bucket requirements
        if category.transaction_type.sign == TransactionType.Sign.POSITIVE and not split_income and not bucket:
            errors['bucket'] = "Bucket is required on positive non-split transactions."
        if category.transaction_type.sign == TransactionType.Sign.NEGATIVE and not bucket:
            errors['bucket'] = "Bucket is required on negative transactions."

        # Validate split_income rules
        if category.transaction_type.sign == TransactionType.Sign.POSITIVE:
            if split_income and not Bucket.is_allocation_complete(user):
                errors['split_income'] = "Cannot create a positive transaction and split it, until bucket allocations sum to 100%. Please complete your bucket allocations first."
        else:
            if split_income:
                errors['split_income'] = "Cannot split negative or neutral transactions. Split is only allowed for positive transactions. Uncheck the 'Split income' box, or choose another category with positive transaction type."

        if errors:
            raise serializers.ValidationError(errors)

        return data
