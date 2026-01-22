import hashlib
import hmac
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from src.application.ports.otp import OtpRecord, OtpRepositoryPort
from src.infrastructure.persistence.models import LoginOtp


class DjangoLoginOtpRepository(OtpRepositoryPort):
    """
    OTP persistence using Django ORM.
    Hashing uses HMAC-SHA256 with a provided secret.
    """

    def __init__(self, *, secret: str) -> None:
        self._secret = secret.encode("utf-8")

    def _hash(self, code: str) -> str:
        return hmac.new(self._secret, code.encode("utf-8"), hashlib.sha256).hexdigest()

    def create_login_otp(self, *, phone: str, code: str, ttl_seconds: int) -> None:
        now = timezone.now()
        LoginOtp.objects.create(
            phone=phone,
            code_hash=self._hash(code),
            expires_at=now + timedelta(seconds=ttl_seconds),
            attempts=0,
        )

    def get_latest_active(self, *, phone: str) -> OtpRecord | None:
        now = timezone.now()
        row = (
            LoginOtp.objects.filter(phone=phone, expires_at__gt=now, consumed_at__isnull=True)
            .order_by("-created_at")
            .first()
        )
        if not row:
            return None
        return OtpRecord(
            phone=row.phone,
            created_at_ts=row.created_at.timestamp(),
            expires_at_ts=row.expires_at.timestamp(),
            attempts=int(row.attempts),
            consumed=row.is_consumed,
        )

    def verify_and_consume(self, *, phone: str, code: str, max_attempts: int) -> bool:
        now = timezone.now()
        code_hash = self._hash(code)
        with transaction.atomic():
            row = (
                LoginOtp.objects.select_for_update()
                .filter(phone=phone, expires_at__gt=now, consumed_at__isnull=True)
                .order_by("-created_at")
                .first()
            )
            if not row:
                return False
            if row.attempts >= max_attempts:
                return False

            row.attempts = int(row.attempts) + 1
            if hmac.compare_digest(row.code_hash, code_hash):
                row.consumed_at = now
                row.save(update_fields=["attempts", "consumed_at"])
                return True
            row.save(update_fields=["attempts"])
            return False

