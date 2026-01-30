import uuid
from django.db import models
from django.utils import timezone

from .media import SbMedia


class SbBanner(models.Model):
    """
    Banner model referencing SbMedia (stored in R2). Designed to be CDN-friendly:
    clients should use the media_url directly (R2 public URL).
    """
    # placement choices can be extended
    HOME_TOP = "HOME_TOP"
    HOME_MIDDLE = "HOME_MIDDLE"
    CATEGORY = "CATEGORY"
    PRODUCT = "PRODUCT"
    PLACEMENT_CHOICES = [
        (HOME_TOP, "Home Top"),
        (HOME_MIDDLE, "Home Middle"),
        (CATEGORY, "Category"),
        (PRODUCT, "Product"),
    ]

    PLATFORM_ANDROID = "android"
    PLATFORM_IOS = "ios"
    PLATFORM_WEB = "web"
    PLATFORM_CHOICES = [
        (PLATFORM_ANDROID, "Android"),
        (PLATFORM_IOS, "iOS"),
        (PLATFORM_WEB, "Web"),
    ]

    TARGET_NONE = "none"
    TARGET_CATEGORY = "category"
    TARGET_PRODUCT = "product"
    TARGET_EXTERNAL = "external_url"
    TARGET_CHOICES = [
        (TARGET_NONE, "None"),
        (TARGET_CATEGORY, "Category"),
        (TARGET_PRODUCT, "Product"),
        (TARGET_EXTERNAL, "External URL"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, blank=True)
    media = models.ForeignKey("persistence.SbMedia", on_delete=models.RESTRICT)
    placement = models.CharField(max_length=40, choices=PLACEMENT_CHOICES)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    target_type = models.CharField(max_length=30, choices=TARGET_CHOICES, default=TARGET_NONE)
    target_value = models.CharField(max_length=1000, null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sb_banner"
        indexes = [
            models.Index(fields=["placement"], name="idx_sb_banner_placement"),
            models.Index(fields=["platform"], name="idx_sb_banner_platform"),
            models.Index(fields=["is_active"], name="idx_sb_banner_active"),
        ]
        ordering = ["-priority", "-created_at"]

    def is_currently_active(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_at and self.start_at > now:
            return False
        if self.end_at and self.end_at < now:
            return False
        return True

    def clean(self):
        # Validate target and media constraints
        from django.core.exceptions import ValidationError

        if self.media.media_type == SbMedia.VIDEO and not self.media.poster_url:
            raise ValidationError("Video media must have a poster_url")
        if self.target_type == self.TARGET_EXTERNAL and not self.target_value:
            raise ValidationError("External URL target requires target_value")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.placement} [{self.platform}] - {self.title or self.media.media_url}"

