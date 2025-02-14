from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from transactions.models import TransactionType
from transactions.models import Category
from transactions.models import Transaction
from transactions.serializers import TransactionTypeSerializer
from transactions.serializers import TransactionTypeWriteSerializer
from transactions.serializers import CategorySerializer
from transactions.serializers import CategoryWriteSerializer
from transactions.serializers import TransactionListSerializer
from transactions.serializers import TransactionDetailSerializer
from transactions.serializers import TransactionWriteSerializer


class TransactionTypeViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    """TransactionType model view."""

    serializer_class = TransactionTypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("name",)

    def get_queryset(self):
        """
        Return all transaction types if user is superuser,
        otherwise return only user's transaction types.
        For anonymous users return empty queryset.
        """
        if not self.request.user.is_authenticated:
            return TransactionType.available_objects.none()
        if self.request.user.is_superuser:
            return TransactionType.available_objects.all()
        return TransactionType.available_objects.filter(user=self.request.user)

    def get_serializer_map(self):
        return {
            "list": TransactionTypeSerializer,
            "retrieve": TransactionTypeSerializer,
            "create": TransactionTypeWriteSerializer,
        }

    def get_serializer_class(self):
        return self.get_serializer_map().get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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


class TransactionViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    """Transaction model view."""

    serializer_class = TransactionListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("name",)

    def get_queryset(self):
        """
        Return all transactions if user is superuser,
        otherwise return only user's transactions.
        For anonymous users return empty queryset.
        """
        if not self.request.user.is_authenticated:
            return Transaction.objects.none()
        if self.request.user.is_superuser:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=self.request.user)

    def get_serializer_map(self):
        return {
            "list": TransactionListSerializer,
            "retrieve": TransactionDetailSerializer,
            "create": TransactionWriteSerializer,
        }

    def get_serializer_class(self):
        return self.get_serializer_map().get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
