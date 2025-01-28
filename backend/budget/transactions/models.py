from django.db import models
from model_utils.models import UUIDModel
from model_utils.models import SoftDeletableModel
from model_utils.models import SoftDeletableManager

from accounts.models import User
from core.models import Bucket


class Entry(UUIDModel):
    """Model to store transaction entry/type information"""

    class Name:
        """Choices for the name field"""

        EXPENSE = "Expense"
        INCOME = "Income"
        TRANSFER = "Transfer"

        CHOICES = (
            (EXPENSE, EXPENSE),
            (INCOME, INCOME),
            (TRANSFER, TRANSFER),
        )

    name = models.CharField(
        max_length=100,
        choices=Name.CHOICES,
        default=Name.EXPENSE,
        blank=False,
        help_text="Transaction type",
        unique=True,
    )

    def __str__(self):
        """Return the string representation of the model"""

        return f"{self.name}"

    class Meta:
        verbose_name = "Entry"
        verbose_name_plural = "Entries"
        ordering = ("name",)


class Category(UUIDModel, SoftDeletableModel):
    """Model to store category information."""

    available_objects = SoftDeletableManager()

    # 'uuid' field is inherited from UUIDModel
    # 'is_removed' field is inherited from SoftDeletableModel

    name = models.CharField(
        help_text="Category name (e.g. (1) for Income: Salary, Bonuses, etc.; (2) for Expense: Utilities, Necessities/Utilities, Books, Education/Books, etc.",
        max_length=255,
        unique=True,
        blank=True,
    )
    bucket = models.ForeignKey(
        Bucket,
        on_delete=models.SET_NULL,
        related_name="categories",
        blank=False,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="categories",
        blank=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("name",)