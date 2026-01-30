import uuid
from django.db import models


class SbMedia(models.Model):
    """
    Reusable media model storing external Cloudflare R2 URLs.
    Media is uploaded externally (R2) and Django stores only URLs.
    """
    IMAGE = "image"
    VIDEO = "video"
    MEDIA_TYPE_CHOICES = [(IMAGE, "Image"), (VIDEO, "Video")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    media_url = models.URLField(max_length=1000)
    poster_url = models.URLField(max_length=1000, null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)  # seconds, for video
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sb_media"
        indexes = [
            models.Index(fields=["media_type"], name="idx_sb_media_type"),
        ]

    def clean(self):
        # Ensure videos have posters
        from django.core.exceptions import ValidationError

        if self.media_type == self.VIDEO and not self.poster_url:
            raise ValidationError("poster_url is required for video media")

    def save(self, *args, **kwargs):
        # enforce validation on save
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.media_type} - {self.media_url}"

