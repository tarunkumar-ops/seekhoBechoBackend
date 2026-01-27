from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class OtpRecord:
    phone: str
    created_at_ts: float
    expires_at_ts: float
    attempts: int
    consumed: bool


class OtpRepositoryPort(Protocol):
    def create_login_otp(self, *, phone: str, code: str, ttl_seconds: int) -> None: ...
    def get_latest_active(self, *, phone: str) -> OtpRecord | None: ...
    def verify_and_consume(self, *, phone: str, code: str, max_attempts: int) -> bool: ...


class OtpSenderPort(Protocol):
    def send_whatsapp_otp(self, *, to_phone: str, code: str, expires_in_minutes: int) -> None: ...
    def send_email_otp(self, *, to_email: str, code: str, expires_in_minutes: int) -> None: ...

