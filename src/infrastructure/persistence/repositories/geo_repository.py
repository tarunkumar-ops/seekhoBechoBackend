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
        return [CityDto(id=int(c.id), title=c.title) for c in qs]

