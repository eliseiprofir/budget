from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.models import Bucket
from core.models import Location
from core.serializers import BucketSerializer
from core.serializers import BucketWriteSerializer
from core.serializers import LocationSerializer
from core.serializers import LocationWriteSerializer


class BucketViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    """Bucket model view."""

    serializer_class = BucketSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("name",)

    def get_queryset(self):
        """
        Return all buckets if user is superuser,
        otherwise return only user's buckets.
        For anonymous users return empty queryset.
        """
        if not self.request.user.is_authenticated:
            return Bucket.available_objects.none()
        if self.request.user.is_superuser:
            return Bucket.available_objects.all()
        return Bucket.available_objects.filter(user=self.request.user)

    def get_serializer_map(self):
        return {
            "list": BucketSerializer,
            "retrieve": BucketSerializer,
            "create": BucketWriteSerializer,
        }

    def get_serializer_class(self):
        return self.get_serializer_map().get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LocationViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    """Location model view."""

    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("name",)

    def get_queryset(self):
        """
        Return all locations if user is superuser,
        otherwise return only user's locations.
        For anonymous users return empty queryset.
        """
        if not self.request.user.is_authenticated:
            return Location.available_objects.none()
        if self.request.user.is_superuser:
            return Location.available_objects.all()
        return Location.available_objects.filter(user=self.request.user)

    def get_serializer_map(self):
        return {
            "list": LocationSerializer,
            "retrieve": LocationSerializer,
            "create": LocationWriteSerializer,
        }

    def get_serializer_class(self):
        return self.get_serializer_map().get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
