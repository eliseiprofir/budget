from django.db import models
from django.core.exceptions import ValidationError
from model_utils.models import UUIDModel
from model_utils.models import SoftDeletableModel
from model_utils.models import SoftDeletableManager

from datetime import date

from accounts.models import User
from core.models import Location
from core.models import Bucket

from utils.strings import truncate


class TransactionType(UUIDModel, SoftDeletableModel):
    """Model to store category information."""

    available_objects = SoftDeletableManager()

    # 'uuid' field is inherited from UUIDModel
    # 'is_removed' field is inherited from SoftDeletableModel

    class Sign:
        """Choices for the sign field"""

        POSITIVE = "POSITIVE"
        NEGATIVE = "NEGATIVE"
        NEUTRAL = "NEUTRAL"

        CHOICES = (
            (POSITIVE, POSITIVE),
            (NEGATIVE, NEGATIVE),
            (NEUTRAL,NEUTRAL)
        )

    sign = models.CharField(
        max_length=20,
        choices=Sign.CHOICES,
        default=Sign.NEUTRAL,
        help_text="Specifies the nature of the transactions. POSITIVE: money coming in, NEGATIVE: money going out, or NEUTRAL: moving between locations/buckets.",
        blank=False,
    )
    name = models.CharField(
        help_text="Transaction type name (e.g. Income, Expense, Transfer, etc.)",
        max_length=255,
        blank=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transaction_types",
        blank=False,
    )

    def save(self, *args, **kwargs):
        if self.pk and TransactionType.all_objects.filter(pk=self.pk).exists():
            old_instance = TransactionType.all_objects.get(pk=self.pk)
            if old_instance.sign != self.sign:
                raise ValidationError("The 'sign' field cannot be changed after creation.")
        super().save(*args, **kwargs)

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
        blank=False,
    )
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.CASCADE,
        related_name="categories",
        blank=False,
        null=False,
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
        default=date.today,
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

    @property
    def transaction_type(self):
        """Return the transaction_type from the related Category."""

        return str(self.category.transaction_type) if self.category else None

    @transaction_type.setter
    def transaction_type(self, value):
        pass

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
