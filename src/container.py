from django.conf import settings

from src.application.use_cases.request_login_otp import RequestLoginOtpUseCase
from src.application.use_cases.verify_login_otp import VerifyLoginOtpUseCase
from src.infrastructure.auth.jwt_provider import SimpleJwtTokenProvider
from src.infrastructure.messaging.whatsapp_sender import (
    DevLoggingWhatsAppOtpSender,
    TwilioWhatsAppOtpSender,
)
from src.infrastructure.messaging.sendgrid_sender import SendGridEmailOtpSender
from src.infrastructure.messaging.composite_sender import CompositeOtpSender

from src.infrastructure.persistence.repositories.otp_repository import DjangoLoginOtpRepository
from src.infrastructure.persistence.repositories.user_repository import DjangoUserRepository
from src.application.use_cases.refresh_tokens import RefreshTokensUseCase
from src.infrastructure.persistence.repositories.geo_repository import DjangoGeoRepository
from src.infrastructure.persistence.repositories.banner_repository import DjangoBannerRepository
from src.application.use_cases.list_states import ListStatesUseCase
from src.application.use_cases.list_cities import ListCitiesUseCase
from src.application.use_cases.list_cities_with_state import ListCitiesWithStateUseCase
from src.application.use_cases.list_cities_search import ListCitiesSearchUseCase
from src.application.use_cases.get_prefill_config import GetPrefillConfigUseCase
from src.application.use_cases.get_user_details import GetUserDetailsUseCase
from src.application.use_cases.update_user_details import UpdateUserDetailsUseCase
from src.infrastructure.persistence.repositories.config_repository import DjangoConfigRepository
from src.infrastructure.storage.r2_service import R2Service
from src.application.use_cases.presign_media import PresignMediaUseCase
from src.application.use_cases.confirm_media import ConfirmMediaUseCase
from src.infrastructure.persistence.repositories.media_repository import DjangoMediaRepository


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
        # Also configure email sender (SendGrid) and wrap into composite
        email_sender = SendGridEmailOtpSender()
        self._otp_sender = CompositeOtpSender(whatsapp_sender=self._otp_sender, email_sender=email_sender)
        # Geo repo
        self._geo_repo = DjangoGeoRepository()
        # Config repo (occupations / platforms)
        self._config_repo = DjangoConfigRepository()
        # Banner repo
        self._banner_repo = DjangoBannerRepository()
        # R2 service
        self._r2_service = R2Service()
        # Media repo
        self._media_repo = DjangoMediaRepository()

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

    def list_states(self) -> ListStatesUseCase:
        return ListStatesUseCase(geo_repo=self._geo_repo)

    def list_cities(self) -> ListCitiesUseCase:
        return ListCitiesUseCase(geo_repo=self._geo_repo)

    def list_cities_with_state(self) -> ListCitiesWithStateUseCase:
        return ListCitiesWithStateUseCase(geo_repo=self._geo_repo)

    def list_cities_search(self) -> ListCitiesSearchUseCase:
        return ListCitiesSearchUseCase(geo_repo=self._geo_repo)

    def get_prefill_config(self) -> GetPrefillConfigUseCase:
        return GetPrefillConfigUseCase(repo=self._config_repo)

    def list_banners(self) -> "ListBannersUseCase":
        from src.application.use_cases.list_banners import ListBannersUseCase
        return ListBannersUseCase(banner_repo=self._banner_repo)

    def create_banner(self):
        from src.application.use_cases.create_banner import CreateBannerUseCase

        return CreateBannerUseCase(banner_repo=self._banner_repo)

    def presign_media(self) -> PresignMediaUseCase:
        return PresignMediaUseCase(r2_service=self._r2_service)

    def confirm_media(self) -> ConfirmMediaUseCase:
        return ConfirmMediaUseCase(media_repo=self._media_repo)

    def get_user_details(self) -> GetUserDetailsUseCase:
        return GetUserDetailsUseCase(user_repo=self._user_repo)

    def update_user_details(self) -> UpdateUserDetailsUseCase:
        return UpdateUserDetailsUseCase(user_repo=self._user_repo)


_container: Container | None = None


def get_container() -> Container:
    global _container
    if _container is None:
        _container = Container()
    return _container

