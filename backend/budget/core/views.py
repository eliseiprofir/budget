from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.models import Bucket
from core.models import Location
from core.serializers import BucketSerializer
from core.serializers import BucketWriteSerializer
from core.serializers import LocationSerializer
from core.serializers import LocationWriteSerializer


class LocationViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """Location model view."""
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("name",)

    def get_queryset(self):
        """Retrieve a custom queryset for locations based on the current user."""
        return Location.available_objects.filter_by_user(self.request.user)

    def get_serializer_map(self):
        return {
            "list": LocationSerializer,
            "retrieve": LocationSerializer,
            "create": LocationWriteSerializer,
            "update": LocationWriteSerializer,
            "partial_update": LocationWriteSerializer,
        }

    def get_serializer_class(self):
        return self.get_serializer_map().get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class BucketViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """Bucket model view."""
    serializer_class = BucketSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("name",)

    def get_queryset(self):
        """Retrieve a custom queryset for buckets based on the current user."""
        return Bucket.available_objects.filter_by_user(user=self.request.user)

    def get_serializer_map(self):
        return {
            "list": BucketSerializer,
            "retrieve": BucketSerializer,
            "create": BucketWriteSerializer,
            "update": BucketWriteSerializer,
            "partial_update": BucketWriteSerializer,
        }

    def get_serializer_class(self):
        return self.get_serializer_map().get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
