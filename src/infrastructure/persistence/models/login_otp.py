from django.db import models


class LoginOtp(models.Model):
    phone = models.CharField(max_length=32, db_index=True)
    code_hash = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    consumed_at = models.DateTimeField(null=True, blank=True)
    attempts = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["phone", "-created_at"]),
        ]

    @property
    def is_consumed(self) -> bool:
        return self.consumed_at is not None

