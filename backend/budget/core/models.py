from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from model_utils.models import UUIDModel
from model_utils.models import SoftDeletableModel
from model_utils.models import SoftDeletableManager

from accounts.models import User


class Bucket(UUIDModel, SoftDeletableModel):
    """Model to store bucket information."""

    available_objects = SoftDeletableManager()

    # 'uuid' field is inherited from UUIDModel
    # 'is_removed' field is inherited from SoftDeletableModel

    class AllocationStatus:
        """Choices for the allocation_status field"""

        INCOMPLETE = "INCOMPLETE"
        COMPLETE = "COMPLETE"

        CHOICES = (
            (INCOMPLETE, INCOMPLETE),
            (COMPLETE, COMPLETE),
        )

    name = models.CharField(
        help_text="Bucket name (e.g. Economy, Necessities, Education, Donation, etc.)",
        max_length=255,
        blank=False,
        null=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="buckets",
        blank=False,
        null=False,
    )
    allocation_percentage = models.DecimalField(
        help_text="Percentage of income to allocate to this bucket",
        max_digits=5,
        decimal_places=2,
        default=0,
        null=False,
    )
    allocation_status = models.CharField(
        max_length=20,
        choices=AllocationStatus.CHOICES,
        default=AllocationStatus.INCOMPLETE,
        help_text="Allocation status for buckets. INCOMPLETE < 100%, COMPLETE = 100%",
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.name

    def get_total_allocation_percentage(self):
        """Get total allocation percentage for user's buckets."""

        user_buckets = Bucket.available_objects.filter(user=self.user)
        return user_buckets.aggregate(total=models.Sum("allocation_percentage"))["total"]

    def get_available_percentage(self):
        """Get remaining percentage available for allocation."""

        return Decimal("100") - self.get_total_allocation_percentage()

    @classmethod
    def is_allocation_complete(cls, user) -> bool:
        """Check if user's bucket allocations sum up to 100%."""

        user_buckets = cls.available_objects.filter(user=user)
        total = user_buckets.aggregate(total=models.Sum("allocation_percentage"))["total"]
        return total == 100

    def validate_name(self):
        """Validate bucket name is unique to current user."""

        existing_query = Bucket.available_objects.filter(
            user=self.user,
            name=self.name
        )
        if self.pk:
            existing_query = existing_query.exclude(pk=self.pk)
        if existing_query.exists():
            raise ValidationError("You already have a bucket with that name.")

    def validate_allocation_percentage(self):
        """Validate allocation_percentage field."""

        # Validate allocation_percentage is between 0 and 100.
        value = self.allocation_percentage
        if value < Decimal("0") or value > Decimal("100"):
            raise ValidationError("Allocation percentage must be between 0 and 100.")

        # Validate sum of all bucket's allocation percentages does not exceed 100%.
        bucket_query = Bucket.available_objects.filter(user=self.user)
        if self.pk:
            bucket_query = bucket_query.exclude(pk=self.pk)
        current_total = bucket_query.aggregate(
            models.Sum("allocation_percentage")
        )["allocation_percentage__sum"] or Decimal("0")
        new_total = current_total + Decimal(self.allocation_percentage)
        if new_total > 100:
            raise ValidationError(f"Total allocation cannot exceed 100%. Allocation left: {100-current_total}%.")

    def clean(self):
        """Validate model as a whole, plus custom validation methods."""

        super().clean()
        self.validate_name()
        self.validate_allocation_percentage()

    def save(self, *args, **kwargs):
        """Save method that checks if all buckets are allocated."""
        self.full_clean()

        super().save(*args, **kwargs)

        total = self.get_total_allocation_percentage()
        new_status = self.AllocationStatus.COMPLETE if total == Decimal("100") else self.AllocationStatus.INCOMPLETE
        Bucket.available_objects.filter(user=self.user).update(allocation_status=new_status)

    class Meta:
        verbose_name = "Bucket"
        verbose_name_plural = "Buckets"
        ordering = ("name",)


class Location(UUIDModel, SoftDeletableModel):
    """Model to store location information."""

    available_objects = SoftDeletableManager()

    # 'uuid' field is inherited from UUIDModel
    # 'is_removed' field is inherited from SoftDeletableModel

    name = models.CharField(
        help_text="Location name (e.g. Cash, Card, Revolut, ING, etc.)",
        max_length=255,
        blank=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="locations",
        blank=False,
    )

    def __str__(self):
        return self.name

    def validate_name(self):
        """Validate location name is unique to current user."""

        existing_query = Location.available_objects.filter(
            user=self.user,
            name=self.name
        )
        if self.pk:
            existing_query = existing_query.exclude(pk=self.pk)
        if existing_query.exists():
            raise ValidationError("You already have a location with that name.")

    def clean(self):
        """Validate model as a whole."""

        super().clean()
        self.validate_name()

    def save(self, *args, **kwargs):
        """Save method plus validate methods."""

        self.full_clean()
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ("name",)
