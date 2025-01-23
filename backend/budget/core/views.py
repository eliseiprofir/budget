from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.models import Bucket
from core.models import Location
from core.serializers import BucketListSerializer
from core.serializers import BucketDetailSerializer
from core.serializers import BucketWriteSerializer
from core.serializers import LocationListSerializer
from core.serializers import LocationDetailSerializer
from core.serializers import LocationWriteSerializer

class BucketViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    """Bucket model view."""

    queryset = Bucket.available_objects.all()
    serializer_class = BucketListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("name",)

    def get_serializer_map(self):
        return {
            "list": BucketListSerializer,
            "retrieve": BucketDetailSerializer,
            "create": BucketWriteSerializer,
        }

    def get_serializer_class(self):
        return self.get_serializer_map().get(self.action, self.serializer_class)


class LocationViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    """Location model view."""

    queryset = Location.available_objects.all()
    serializer_class = LocationListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("name",)

    def get_serializer_map(self):
        return {
            "list": LocationListSerializer,
            "retrieve": LocationDetailSerializer,
            "create": LocationWriteSerializer,
        }

    def get_serializer_class(self):
        return self.get_serializer_map().get(self.action, self.serializer_class)
