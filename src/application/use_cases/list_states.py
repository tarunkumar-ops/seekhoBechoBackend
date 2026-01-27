from src.application.ports.geo import GeoRepositoryPort, StateDto


class ListStatesUseCase:
    def __init__(self, *, geo_repo: GeoRepositoryPort) -> None:
        self._geo_repo = geo_repo

    def execute(self, country_iso2: str) -> list[StateDto]:
        return self._geo_repo.list_states(country_iso2=country_iso2)

