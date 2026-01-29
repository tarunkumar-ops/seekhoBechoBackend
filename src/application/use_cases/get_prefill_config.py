from src.application.ports.config import ConfigRepositoryPort, OccupationDto, PlatformDto


class GetPrefillConfigUseCase:
    def __init__(self, *, repo: ConfigRepositoryPort) -> None:
        self._repo = repo

    def execute(self) -> dict:
        occupations = self._repo.list_occupations()
        platforms = self._repo.list_interested_platforms()
        return {"occupations": occupations, "interested_platforms": platforms}

