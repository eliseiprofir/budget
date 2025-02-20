from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from accounts.serializers import UserListSerializer
from accounts.serializers import UserDetailSerializer
from accounts.serializers import UserWriteSerializer


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    """User model view."""

    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("created",)

    def get_queryset(self):
        """Filter queryset to return only the current user. Superusers can see all users."""

        return User.objects.filter_by_user(self.request.user)

    def get_object(self):
        """Override to ensure users can only retrieve their own profile. Superusers can retrieve any profile."""

        obj = super().get_object()
        if not self.request.user.is_superuser and obj.id != self.request.user.id:
            self.permission_denied(
                self.request,
                message="You do not have permission to access this user's profile."
            )
        return obj

    def get_serializer_map(self):
        return {
            "list": UserListSerializer,
            "retrieve": UserDetailSerializer,
            "create": UserWriteSerializer,
        }

    def get_serializer_class(self):
        return self.get_serializer_map().get(self.action, self.serializer_class)
