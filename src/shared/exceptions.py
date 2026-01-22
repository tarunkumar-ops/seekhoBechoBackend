class AppError(Exception):
    """Base error for application-layer failures."""


class ValidationError(AppError):
    """Raised when input validation fails."""


class AuthError(AppError):
    """Raised when authentication/authorization fails."""

