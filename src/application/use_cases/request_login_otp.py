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

    def execute(self, input_dto: RequestOtpInput) -> dict:
        phone = (input_dto.phone or "").strip() if input_dto.phone else None
        email = (input_dto.email or "").strip() if input_dto.email else None
        if not phone and not email:
            from src.shared.exceptions import ValidationError

            raise ValidationError("phone or email is required")

        code = f"{secrets.randbelow(1_000_000):06d}"
        # store identifier as-is in OTP repo (phone or email)
        identifier = phone or email
        # Persist synchronously
        self._otp_repo.create_login_otp(phone=identifier, code=code, ttl_seconds=self.  _ttl_seconds)
        # Convert ttl_seconds to minutes for message template
        expires_minutes = int((self._ttl_seconds + 59) // 60)
        # Return information so interface layer can dispatch async delivery
        return {"identifier": identifier, "phone": phone, "email": email, "code": code, "expires_minutes": expires_minutes}

