from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from transactions.models import Entry
from transactions.models import Category
from transactions.serializers import EntrySerializer
from transactions.serializers import CategorySerializer
from transactions.serializers import EntryWriteSerializer
from transactions.serializers import CategoryWriteSerializer


class EntryViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    """Entry model view."""

    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("name",)

    def get_serializer_map(self):
        return {
            "list": EntrySerializer,
            "retrieve": EntrySerializer,
            "create": EntryWriteSerializer,
        }

    def get_serializer_class(self):
        return self.get_serializer_map().get(self.action, self.serializer_class)


class CategoryViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    """Category model view."""

    queryset = Category.available_objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("name",)

    def get_serializer_map(self):
        return {
            "list": CategorySerializer,
            "retrieve": CategorySerializer,
            "create": CategoryWriteSerializer,
        }

    def get_serializer_class(self):
        return self.get_serializer_map().get(self.action, self.serializer_class)
