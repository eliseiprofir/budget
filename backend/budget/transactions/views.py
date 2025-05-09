from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from transactions.models import Category
from transactions.models import Transaction
from transactions.serializers import CategorySerializer
from transactions.serializers import CategoryWriteSerializer
from transactions.serializers import TransactionListSerializer
from transactions.serializers import TransactionDetailSerializer
from transactions.serializers import TransactionWriteSerializer

from .permissions import IsOwner


class CategoryViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """Category model view."""

    queryset = Category.available_objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, IsOwner)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("name",)

    def get_queryset(self):
        """Retrieve a custom queryset for categories based on the current user."""
        return Category.available_objects.filter_by_user(self.request.user)

    def get_serializer_map(self):
        return {
            "list": CategorySerializer,
            "retrieve": CategorySerializer,
            "create": CategoryWriteSerializer,
            "update": CategoryWriteSerializer,
            "partial_update": CategoryWriteSerializer,
        }

    def get_serializer_class(self):
        return self.get_serializer_map().get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """Transaction model view."""
    serializer_class = TransactionListSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("name",)

    def get_queryset(self):
        """Retrieve a custom queryset for transactions based on the current user."""
        return Transaction.objects.filter_by_user(self.request.user)

    def get_serializer_map(self):
        return {
            "list": TransactionListSerializer,
            "retrieve": TransactionDetailSerializer,
            "create": TransactionWriteSerializer,
            "update": TransactionWriteSerializer,
            "partial_update": TransactionWriteSerializer,
        }

    def get_serializer_class(self):
        return self.get_serializer_map().get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
