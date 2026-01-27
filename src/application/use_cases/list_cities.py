from src.application.ports.geo import GeoRepositoryPort, CityDto


class ListCitiesUseCase:
    def __init__(self, *, geo_repo: GeoRepositoryPort) -> None:
        self._geo_repo = geo_repo

    def execute(self, state_id: int) -> list[CityDto]:
        return self._geo_repo.list_cities_by_state(state_id=state_id)

