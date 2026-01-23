import secrets

from src.application.dtos.auth_dtos import RequestOtpInput
from src.application.ports.otp import OtpRepositoryPort, OtpSenderPort
from src.domain.value_objects.phone import normalize_e164


class RequestLoginOtpUseCase:
    def __init__(
        self,
        *,
        otp_repo: OtpRepositoryPort,
        otp_sender: OtpSenderPort,
        ttl_seconds: int = 300,
    ) -> None:
        self._otp_repo = otp_repo
        self._otp_sender = otp_sender
        self._ttl_seconds = ttl_seconds

    def execute(self, input_dto: RequestOtpInput) -> None:
        phone = normalize_e164(input_dto.phone)
        code = f"{secrets.randbelow(1_000_000):06d}"
        self._otp_repo.create_login_otp(phone=phone, code=code, ttl_seconds=self._ttl_seconds)
        # Convert ttl_seconds to minutes for message template
        expires_minutes = int((self._ttl_seconds + 59) // 60)
        self._otp_sender.send_whatsapp_otp(to_phone=phone, code=code, expires_in_minutes=expires_minutes)

