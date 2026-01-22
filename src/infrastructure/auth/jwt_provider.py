from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from src.application.ports.auth import TokenPair, TokenProviderPort


class SimpleJwtTokenProvider(TokenProviderPort):
    def issue_tokens_for_user_id(self, *, user_id: int) -> TokenPair:
        User = get_user_model()
        user = User.objects.get(pk=user_id)
        refresh = RefreshToken.for_user(user)
        return TokenPair(access=str(refresh.access_token), refresh=str(refresh))

