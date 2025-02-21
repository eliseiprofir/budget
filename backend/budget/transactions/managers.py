from django.db.models.manager import Manager
from model_utils.managers import SoftDeletableManager

from .queryset import TransactionTypeQuerySet
from .queryset import CategoryQuerySet
from .queryset import TransactionQuerySet


class TransactionTypeManager(SoftDeletableManager.from_queryset(TransactionTypeQuerySet)):
    """TransactionType manager."""
    pass


class CategoryManager(SoftDeletableManager.from_queryset(CategoryQuerySet)):
    """Category manager."""
    pass


class TransactionManager(Manager.from_queryset(TransactionQuerySet)):
    """Transaction manager."""
    pass
