from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from model_utils.models import UUIDModel
from model_utils.models import SoftDeletableModel

from accounts.models import User
from core.models import Location
from core.models import Bucket

from utils.strings import truncate

from .managers import CategoryManager
from .managers import TransactionManager


class Category(UUIDModel, SoftDeletableModel):
    """Model to store category information."""
    available_objects = CategoryManager()

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
            (NEUTRAL, NEUTRAL)
        )

    name = models.CharField(
        help_text="Category name (e.g. (1) for Income: Salary, Bonuses, etc.; (2) for Expense: Utilities, Necessities/Utilities, Books, Education/Books, etc.",
        max_length=255,
        blank=False,
    )
    sign = models.CharField(
        max_length=20,
        choices=Sign.CHOICES,
        default=Sign.NEUTRAL,
        help_text="Specifies the nature of the transactions. POSITIVE: money coming in, NEGATIVE: money going out, or NEUTRAL: moving between locations/buckets.",
        blank=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="categories",
        blank=False,
        null=False,
    )

    def __str__(self):
        """Return the string representation of the model"""
        return self.name

    def validate_name(self):
        """Validate category name is unique to current user."""
        existing_query = Category.available_objects.filter(
            name=self.name,
            user=self.user
        )
        if self.pk:
            existing_query = existing_query.exclude(pk=self.pk)
        if existing_query.exists():
            raise ValidationError("You already have a category with that name.")

    def clean(self):
        """Validate model as a whole."""
        super().clean()
        self.validate_name()

    def save(self, *args, **kwargs):
        """Save method plus validate methods."""
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("name",)


class Transaction(UUIDModel):
    """Model to store transaction entry/type information"""
    objects = TransactionManager()

    # 'uuid' field is inherited from UUIDModel

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
    date = models.DateTimeField(
        blank=False,
        null=False,
        default=now,
        help_text="Transaction date",
    )
    amount = models.DecimalField(
        max_digits=10,
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
        null=True,
        blank=True,
    )
    split_income = models.BooleanField(
        default=False,
        blank=False,
        null=False,
        help_text="Whether to split income into multiple buckets or not (only for positive transactions)."
    )
    parent_transaction = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="split_transactions",
        help_text="Parent transaction for a split positive transaction.",
        db_index=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions",
        blank=False,
        null=False,
    )

    def __str__(self):
        """Return the string representation of the model"""
        return f"{truncate(str(self.description), 15)}: {self.amount}"

    def get_full_info(self):
        """Return all information about the transaction"""
        return f"{self.date}, {self.category.name}, {truncate(str(self.description), 10)}, {self.location}, {self.bucket}"

    def _split_income(self):
        """Split income into multiple transactions based on bucket allocations."""
        Transaction.objects.filter(parent_transaction=self).delete()

        buckets = Bucket.available_objects.filter(user=self.user)

        for bucket in buckets:
            if bucket.allocation_percentage > 0:
                split_amount = (
                    self.amount *
                    bucket.allocation_percentage /
                    Decimal("100")
                ).quantize(Decimal(".01"))

                Transaction.objects.create(
                    user=self.user,
                    description=f"{self.description} ({bucket.allocation_percentage}%)",
                    category=self.category,
                    date=self.date,
                    amount=split_amount,
                    location=self.location,
                    bucket=bucket,
                    parent_transaction=self,
                    split_income=False,
                )

        Transaction.objects.filter(
            pk=self.pk
        ).update(
            amount=0,
            description=f"{self.description} ({self.amount})",
        )

    def validate_user(self):
        """Validate that the user is selected."""
        if not hasattr(self, "user") or not self.user:
            raise ValidationError({
                'user': "User must be specified"
            })

    def validate_bucket(self):
        """Validate bucket field should be selected if not splitting income."""
        if self.category.sign == Category.Sign.POSITIVE and not self.split_income and not self.bucket:
            raise ValidationError({"bucket": "Bucket is required on positive non-split transactions."})
        if self.category.sign == Category.Sign.NEGATIVE and not self.bucket:
            raise ValidationError({"bucket": "Bucket is required on negative transactions."})

    def validate_split_income(self):
        """Validate split_income field for positive transactions."""
        if self.category.sign == Category.Sign.POSITIVE:
            if self.split_income and not Bucket.is_allocation_complete(self.user):
                raise ValidationError({"split_income":"Cannot create a positive transaction and split it, until bucket allocations sum to 100%. Please complete your bucket allocations first."})
        else:
            if self.split_income:
                raise ValidationError({"split_income": "Cannot split negative or neutral transactions. Split is only allowed for positive transactions. Uncheck the 'Split income' box, or choose another category with positive transaction type."})

    def clean(self):
        """Validate model data before saving."""
        super().clean()
        self.validate_user()
        self.validate_bucket()
        self.validate_split_income()

    def save(self, *args, **kwargs):
        """Adjust the amount if the transaction_type is negative"""
        self.full_clean()
        super().save(*args, **kwargs)

        if self.category.sign == Category.Sign.POSITIVE and self.split_income:
            self._split_income()

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ("-date",)
