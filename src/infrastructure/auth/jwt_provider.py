from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from src.application.ports.auth import TokenPair, TokenProviderPort
from src.shared.exceptions import AuthError


class SimpleJwtTokenProvider(TokenProviderPort):
    def issue_tokens_for_user_id(self, *, user_id: int) -> TokenPair:
        User = get_user_model()
        user = User.objects.get(pk=user_id)
        refresh = RefreshToken.for_user(user)
        return TokenPair(access=str(refresh.access_token), refresh=str(refresh))

    def refresh_tokens(self, *, refresh: str) -> TokenPair:
        """
        Validate the provided refresh token and issue a new token pair.
        Raises AuthError if the refresh token is invalid/expired.
        """
        try:
            rt = RefreshToken(refresh)
        except TokenError:
            raise AuthError("invalid or expired refresh token")

        try:
            user_id = int(rt["user_id"])
        except Exception:
            raise AuthError("invalid refresh token payload")

        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise AuthError("user for refresh token not found")

        new_refresh = RefreshToken.for_user(user)
        return TokenPair(access=str(new_refresh.access_token), refresh=str(new_refresh))

