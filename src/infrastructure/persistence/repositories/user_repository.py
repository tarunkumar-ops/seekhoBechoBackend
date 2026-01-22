from django.contrib.auth import get_user_model

from src.application.ports.auth import UserRepositoryPort


class DjangoUserRepository(UserRepositoryPort):
    def get_or_create_user_id_by_phone(self, *, phone: str) -> int:
        """
        Uses Django's default User model. Stores phone in `username` for simplicity.
        If you later add a custom user model, keep this as the only place that changes.
        """
        User = get_user_model()
        user, _ = User.objects.get_or_create(username=phone, defaults={"is_active": True})
        return int(user.id)

