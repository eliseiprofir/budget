from django.db import models
from model_utils.models import UUIDModel
from model_utils.models import SoftDeletableModel
from model_utils.models import SoftDeletableManager

from datetime import datetime

from accounts.models import User
from core.models import Location
from core.models import Bucket

from utils.strings import truncate


class TransactionType(UUIDModel, SoftDeletableModel):
    """Model to store category information."""

    available_objects = SoftDeletableManager()

    # 'uuid' field is inherited from UUIDModel
    # 'is_removed' field is inherited from SoftDeletableModel

    name = models.CharField(
        help_text="Category name (e.g. Income, Expense, Transfer, etc.)",
        max_length=255,
        unique=True,
        blank=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Transaction Type"
        verbose_name_plural = "Transaction Types"
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
        blank=False,
    )
    bucket = models.ForeignKey(
        Bucket,
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


class Transaction(UUIDModel):
    """Model to store transaction entry/type information"""

    # 'uuid' field is inherited from UUIDModel

    class TransactionType:
        """Choices for the transaction_type field"""

        EXPENSE = "Expense"
        INCOME = "Income"
        TRANSFER = "Transfer"
        TEMPORARY = "Temporary"

        CHOICES = (
            (EXPENSE, EXPENSE),
            (INCOME, INCOME),
            (TRANSFER, TRANSFER),
            (TEMPORARY, TEMPORARY),
        )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions",
        blank=False,
        null=False,
    )
    description = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text="Transaction description",
    )
    transaction_type = models.CharField(
        max_length=100,
        choices=TransactionType.CHOICES,
        default=TransactionType.EXPENSE,
        blank=False,
        help_text="Transaction type",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="transactions",
        blank=False,
        null=True,
    )
    date = models.DateField(
        blank=False,
        null=False,
        default=datetime.today,
        help_text="Transaction date",
    )
    amount = models.DecimalField(
        max_digits=1000,
        decimal_places=2,
        blank=False,
        null=False,
        help_text="Transaction amount",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name="transactions",
        blank=False,
        null=True,
    )
    bucket = models.ForeignKey(
        Bucket,
        on_delete=models.SET_NULL,
        related_name="transactions",
        blank=False,
        null=True,
    )

    def __str__(self):
        """Return the string representation of the model"""

        return f"{truncate(str(self.description), 15)}: {self.amount}"

    def get_full_info(self):
        """Return all information about the transaction"""

        return f"{self.date}, {self.transaction_type}, {self.category.name}, {truncate(str(self.description), 10)}, {self.location}, {self.bucket}"


    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ("-date",)
