from typing import List

from src.application.ports.geo import GeoRepositoryPort, StateDto, CityDto
from src.infrastructure.persistence.models import Country, State, City


class DjangoGeoRepository(GeoRepositoryPort):
    def list_states(self, *, country_iso2: str) -> List[StateDto]:
        country = Country.objects.filter(iso2__iexact=country_iso2).first()
        if not country:
            return []
        qs = State.objects.filter(country=country, status=True).order_by("title")
        return [StateDto(id=int(s.id), title=s.title) for s in qs]

    def list_cities_by_state(self, *, state_id: int) -> List[CityDto]:
        qs = City.objects.filter(state_id=state_id, status=True).order_by("title")
        return [CityDto(id=int(c.id), title=c.title, state_id=int(c.state_id), state_title=c.state_name) for c in qs]

    def get_state_by_id(self, *, state_id: int) -> StateDto | None:
        s = State.objects.filter(pk=state_id, status=True).first()
        if not s:
            return None
        return StateDto(id=int(s.id), title=s.title)

    def list_cities_by_query(self, *, q: str) -> List[CityDto]:
        qs = City.objects.filter(title__icontains=q, status=True).order_by("title")
        return [CityDto(id=int(c.id), title=c.title, state_id=int(c.state_id), state_title=c.state_name) for c in qs]

    def get_city_with_state(self, *, city_id: int) -> tuple[CityDto | None, StateDto | None]:
        c = City.objects.filter(pk=city_id, status=True).select_related("state", "country").first()
        if not c:
            return None, None
        city_dto = CityDto(id=int(c.id), title=c.title, state_id=int(c.state_id), state_title=c.state_name)
        state = c.state
        state_dto = StateDto(id=int(state.id), title=state.title) if state else None
        return city_dto, state_dto

