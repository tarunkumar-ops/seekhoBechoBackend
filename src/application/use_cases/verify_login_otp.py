from src.application.dtos.auth_dtos import VerifyOtpInput, VerifyOtpOutput
from src.application.ports.auth import TokenProviderPort, UserRepositoryPort
from src.application.ports.otp import OtpRepositoryPort
from src.domain.value_objects.phone import normalize_e164
from src.shared.exceptions import AuthError, ValidationError


class VerifyLoginOtpUseCase:
    def __init__(
        self,
        *,
        otp_repo: OtpRepositoryPort,
        user_repo: UserRepositoryPort,
        token_provider: TokenProviderPort,
        max_attempts: int = 5,
    ) -> None:
        self._otp_repo = otp_repo
        self._user_repo = user_repo
        self._token_provider = token_provider
        self._max_attempts = max_attempts

    def execute(self, input_dto: VerifyOtpInput) -> VerifyOtpOutput:
        phone = normalize_e164(input_dto.phone)
        code = (input_dto.code or "").strip()
        if len(code) != 6 or not code.isdigit():
            raise ValidationError("code must be 6 digits")

        ok = self._otp_repo.verify_and_consume(phone=phone, code=code, max_attempts=self._max_attempts)
        if not ok:
            raise AuthError("invalid or expired code")

        user_id = self._user_repo.get_or_create_user_id_by_phone(phone=phone)
        tokens = self._token_provider.issue_tokens_for_user_id(user_id=user_id)
        return VerifyOtpOutput(access=tokens.access, refresh=tokens.refresh)

