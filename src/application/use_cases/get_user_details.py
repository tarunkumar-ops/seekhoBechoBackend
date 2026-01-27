from src.application.ports.auth import UserRepositoryPort
from src.application.dtos.auth_dtos import UserDetailsOutput


class GetUserDetailsUseCase:
    def __init__(self, *, user_repo: UserRepositoryPort) -> None:
        self._user_repo = user_repo

    def execute(self, user_id: int) -> UserDetailsOutput | None:
        data = self._user_repo.get_user_by_id(user_id=user_id)
        if not data:
            return None
        return UserDetailsOutput(**data)

