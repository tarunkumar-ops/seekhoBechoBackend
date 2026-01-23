from src.application.dtos.auth_dtos import RefreshTokenInput, RefreshTokenOutput
from src.application.ports.auth import TokenProviderPort


class RefreshTokensUseCase:
    def __init__(self, *, token_provider: TokenProviderPort) -> None:
        self._token_provider = token_provider

    def execute(self, input_dto: RefreshTokenInput) -> RefreshTokenOutput:
        tokens = self._token_provider.refresh_tokens(refresh=input_dto.refresh)
        return RefreshTokenOutput(access=tokens.access, refresh=tokens.refresh)

