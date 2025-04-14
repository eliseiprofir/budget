from rest_framework import serializers

from .models import User


class UserListSerializer(serializers.ModelSerializer):
    """List Serializer for the User Model"""

    class Meta:
        model = User
        fields = ("id", "email", "full_name", "is_active")
        read_only_fields = fields


class UserDetailSerializer(serializers.ModelSerializer):
    """Detail Serializer for the User Model"""

    class Meta(UserListSerializer.Meta):
        fields = (*UserListSerializer.Meta.fields, "password", "last_login", "created", "modified")
        read_only_fields = fields


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer used specifically for create operations"""
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "full_name", "password")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data.get("full_name", "")
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer used specifically for update operations"""
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("email", "full_name", "password")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
