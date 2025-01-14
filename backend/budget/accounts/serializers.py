from rest_framework import serializers

from backend.budget.accounts.models import User

class UserListSerializer(serializers.ModelSerializer):
    """List Serializer for the User Model"""

    class Meta:
        model = User
        fields = ("id", "email", "full_name", "is_active")
        read_only_fields = fields


class UserDetailSerializer(serializers.ModelSerializer):
    """Detail Serializer for the User Model"""

    class Meta(UserListSerializer.Meta):
        fields = (*UserListSerializer.Meta.fields, "last_login", "created", "modified")
        read_only_fields = fields


class UserWriteSerializer(serializers.ModelSerializer):
    """Serializer used for create operations"""

    class Meta:
        model = User
        fields = ("full_name", "email")
        read_only_fields = ("id",)
