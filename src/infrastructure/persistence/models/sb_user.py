from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .user_manager import SbUserManager


class SbUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = "sb_users"
        indexes = [
            models.Index(fields=["language"]),
        ]

    id = models.BigAutoField(primary_key=True)

    user_code = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=150)

    whatsapp_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=190, null=True, blank=True)

    # --- Foreign Keys ---
    country = models.ForeignKey(
        "persistence.Country",
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )
    state = models.ForeignKey(
        "persistence.State",
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )
    city = models.ForeignKey(
        "persistence.City",
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )
    platform = models.ForeignKey(
        "persistence.InterestedPlatform",
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )
    occupation = models.ForeignKey(
        "persistence.Occupation",
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )
    language = models.ForeignKey(
        "persistence.Language",
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )

    # --- Denormalized names ---
    country_name = models.CharField(max_length=190, null=True, blank=True)
    state_name = models.CharField(max_length=190, null=True, blank=True)
    city_name = models.CharField(max_length=190, null=True, blank=True)
    platform_name = models.CharField(max_length=190, null=True, blank=True)
    occupation_name = models.CharField(max_length=190, null=True, blank=True)
    language_name = models.CharField(max_length=190, null=True, blank=True)

    budget_to_invest = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    gender = models.CharField(max_length=50)

    # --- Django auth flags ---
    status = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SbUserManager()

    USERNAME_FIELD = "whatsapp_number"
    REQUIRED_FIELDS = ["full_name", "user_code"]

    def __str__(self):
        return self.whatsapp_number
