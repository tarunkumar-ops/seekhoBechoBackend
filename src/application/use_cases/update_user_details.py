from src.application.ports.auth import UserRepositoryPort
from src.application.dtos.auth_dtos import UpdateUserInput, UserDetailsOutput


class UpdateUserDetailsUseCase:
    def __init__(self, *, user_repo: UserRepositoryPort) -> None:
        self._user_repo = user_repo

    def execute(self, user_id: int, input_dto: UpdateUserInput) -> UserDetailsOutput | None:
        # convert dataclass to dict excluding None
        data = {k: v for k, v in input_dto.__dict__.items() if v is not None}
        updated = self._user_repo.update_user(user_id=user_id, data=data)
        if not updated:
            return None
        return UserDetailsOutput(**updated)

