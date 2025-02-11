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

    name = models.CharField(
        help_text="Bucket name (e.g. Economy, Necessities, Education, Donation, etc.)",
        max_length=255,
        blank=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="buckets",
        blank=False,
    )
    allocation_percentage = models.DecimalField(
        help_text="Percentage of income to allocate to this bucket",
        max_digits=5,
        decimal_places=2,
        null=True,
    )

    def __str__(self):
        return self.name

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

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ("name",)
