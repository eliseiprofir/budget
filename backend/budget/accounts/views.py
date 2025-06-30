from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from accounts.models import User
from accounts.serializers import UserListSerializer
from accounts.serializers import UserDetailSerializer
from accounts.serializers import UserCreateSerializer
from accounts.serializers import UserUpdateSerializer

from .permissions import IsOwner


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
):
    """User model view."""
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("created",)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_fields = ("created", "last_login",)
    ordering_fields = ("full_name", "email",)
    search_fields = ("full_name", "email")

    def get_permissions(self):
        """Return permissions depending on action."""
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Retrieve a custom queryset for users based on the current user."""
        if self.action == "list" and not self.request.user.is_authenticated:
            return User.objects.none()
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
            "create": UserCreateSerializer,
            "update": UserUpdateSerializer,
            "partial_update": UserUpdateSerializer,
        }

    def get_serializer_class(self):
        return self.get_serializer_map().get(self.action, self.serializer_class)
