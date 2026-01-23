from django.conf import settings

from src.application.use_cases.request_login_otp import RequestLoginOtpUseCase
from src.application.use_cases.verify_login_otp import VerifyLoginOtpUseCase
from src.infrastructure.auth.jwt_provider import SimpleJwtTokenProvider
from src.infrastructure.messaging.whatsapp_sender import (
    DevLoggingWhatsAppOtpSender,
    TwilioWhatsAppOtpSender,
)
from src.infrastructure.persistence.repositories.otp_repository import DjangoLoginOtpRepository
from src.infrastructure.persistence.repositories.user_repository import DjangoUserRepository
from src.application.use_cases.refresh_tokens import RefreshTokensUseCase


class Container:
    def __init__(self) -> None:
        otp_secret = getattr(settings, "OTP_SECRET", "dev-otp-secret")

        self._otp_repo = DjangoLoginOtpRepository(secret=otp_secret)
        self._user_repo = DjangoUserRepository()
        self._token_provider = SimpleJwtTokenProvider()

        if getattr(settings, "TWILIO_ENABLED", False):
            self._otp_sender = TwilioWhatsAppOtpSender(
                account_sid=getattr(settings, "TWILIO_ACCOUNT_SID", ""),
                auth_token=getattr(settings, "TWILIO_AUTH_TOKEN", ""),
                from_whatsapp=getattr(settings, "TWILIO_WHATSAPP_FROM", ""),
            )
        else:
            self._otp_sender = DevLoggingWhatsAppOtpSender()

    def request_login_otp(self) -> RequestLoginOtpUseCase:
        return RequestLoginOtpUseCase(otp_repo=self._otp_repo, otp_sender=self._otp_sender)

    def verify_login_otp(self) -> VerifyLoginOtpUseCase:
        return VerifyLoginOtpUseCase(
            otp_repo=self._otp_repo,
            user_repo=self._user_repo,
            token_provider=self._token_provider,
        )

    def refresh_tokens(self) -> RefreshTokensUseCase:
        return RefreshTokensUseCase(token_provider=self._token_provider)


_container: Container | None = None


def get_container() -> Container:
    global _container
    if _container is None:
        _container = Container()
    return _container

