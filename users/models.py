from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """
    Custom user manager where email is the unique identifier
    instead of username for authentication.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")

        # Normalize email (lowercase domain part)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        # Set default values for superuser permissions
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email as the username field.

    - AbstractBaseUser: Provides core authentication functionality
    - PermissionsMixin: Adds permission and group support
    """

    email = models.EmailField(
        "email address",
        unique=True,  # Email must be unique across all users
        help_text="Required. Enter a valid email address.",
    )

    first_name = models.CharField("first name", max_length=150, blank=True)
    last_name = models.CharField("last name", max_length=150, blank=True)

    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into the admin site.",
    )

    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active.",
    )

    date_joined = models.DateTimeField("date joined", default=timezone.now)

    # Link the custom manager
    objects = CustomUserManager()

    # Tell Django to use email as the username field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Email is already required as USERNAME_FIELD

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
