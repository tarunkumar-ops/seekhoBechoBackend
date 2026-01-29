from typing import Optional

from src.application.ports.geo import GeoRepositoryPort


class ListCitiesSearchUseCase:
    def __init__(self, *, geo_repo: GeoRepositoryPort) -> None:
        self._geo_repo = geo_repo

    def execute(self, *, q: Optional[str] = None, city_id: Optional[int] = None):
        if city_id is not None:
            city, state = self._geo_repo.get_city_with_state(city_id=city_id)
            return {"city": city, "state": state}
        if q:
            cities = self._geo_repo.list_cities_by_query(q=q)
            return {"cities": cities}
        return {"cities": []}

