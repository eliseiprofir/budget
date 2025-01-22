from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import User
from .serializers import UserListSerializer
from .serializers import UserDetailSerializer
from .serializers import UserWriteSerializer

class UserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    """User model view."""

    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("created",)

    def get_serializer_map(self):
        return {
            "list": UserListSerializer,
            "retrieve": UserDetailSerializer,
            "create": UserWriteSerializer,
        }

    def get_serializer_class(self):
        return self.get_serializer_map().get(self.action, self.serializer_class)
