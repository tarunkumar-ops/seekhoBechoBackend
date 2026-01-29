from src.application.ports.geo import GeoRepositoryPort, StateDto, CityDto


class ListCitiesWithStateUseCase:
    def __init__(self, *, geo_repo: GeoRepositoryPort) -> None:
        self._geo_repo = geo_repo

    def execute(self, state_id: int) -> tuple[StateDto | None, list[CityDto]]:
        state = self._geo_repo.get_state_by_id(state_id=state_id)
        cities = self._geo_repo.list_cities_by_state(state_id=state_id)
        return state, cities

