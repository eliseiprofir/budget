from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.utils import timezone
from model_utils.models import UUIDModel
from model_utils.models import TimeStampedModel
from model_utils.models import SoftDeletableModel
from .managers import UserManager

class User(UUIDModel, AbstractUser, TimeStampedModel, SoftDeletableModel):
    """Model to store user information"""

    # 'uuid' field is inherited from UUIDModel
    # 'created' field is inherited from TimeStampModel
    # 'modified' field is inherited from TimeStampModel
    # 'is_removed' field is inherited from SoftDeletableModel
    # 'is_active' field is inherited from AbstractUser
    # Disable unnecessary AbstractUser fields
    username = None
    first_name = None
    last_name = None

    full_name = models.CharField(
        help_text="Full name",
        max_length=255,
        blank=True,
    )
    email = models.EmailField(
        help_text="Email address",
        max_length=100,
        validators=[EmailValidator(message="Insert a valid email.")],
        unique=True,
        db_index=True,
    )
    last_login = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Last time the user logged in.",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("full_name",)

    objects: UserManager = UserManager()

    def __str__(self) -> str:
        """Return the string representation of the model"""
        if not self.full_name:
            return f"No name ({self.email})"
        return f"{self.full_name} ({self.email})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("-created",)

    def clean_email(self) -> None:
        """Ensure that the email is lowercase"""
        if self.email:
            self.email = f"{self.email}".lower()

    def update_last_login(self) -> None:
        """Update the last_login field to the current timestamp"""
        self.last_login = timezone.now()
        self.save()
