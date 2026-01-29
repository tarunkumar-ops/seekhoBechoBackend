from typing import List
from django.conf import settings
from django.db.models import Q

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
        # Respect configured default country ISO2
        country_iso2 = getattr(settings, "GEO_DEFAULT_COUNTRY_ISO2", "IN")
        iso_list = [s.strip() for s in country_iso2.split(",") if s.strip()]
        if iso_list:
            q_country = Q()
            for iso in iso_list:
                q_country |= Q(country__iso2__iexact=iso)
            qs = City.objects.filter(q_country, state_id=state_id, status=True).order_by("title")[:20]
        else:
            qs = City.objects.filter(state_id=state_id, status=True).order_by("title")[:20]
        return [CityDto(id=int(c.id), title=c.title, state_id=int(c.state_id), state_title=c.state_name) for c in qs]

    def get_state_by_id(self, *, state_id: int) -> StateDto | None:
        s = State.objects.filter(pk=state_id, status=True).first()
        if not s:
            return None
        return StateDto(id=int(s.id), title=s.title)

    def list_cities_by_query(self, *, q: str) -> List[CityDto]:
        country_iso2 = getattr(settings, "GEO_DEFAULT_COUNTRY_ISO2", "IN")
        iso_list = [s.strip() for s in country_iso2.split(",") if s.strip()]
        if iso_list:
            q_country = Q()
            for iso in iso_list:
                q_country |= Q(country__iso2__iexact=iso)
            qs = City.objects.filter(q_country, title__icontains=q, status=True).order_by("title")[:20]
        else:
            qs = City.objects.filter(title__icontains=q, status=True).order_by("title")[:20]
        return [CityDto(id=int(c.id), title=c.title, state_id=int(c.state_id), state_title=c.state_name) for c in qs]

    def get_city_with_state(self, *, city_id: int) -> tuple[CityDto | None, StateDto | None]:
        country_iso2 = getattr(settings, "GEO_DEFAULT_COUNTRY_ISO2", "IN")
        iso_list = [s.strip() for s in country_iso2.split(",") if s.strip()]
        if iso_list:
            q_country = Q()
            for iso in iso_list:
                q_country |= Q(country__iso2__iexact=iso)
            c = City.objects.filter(q_country, pk=city_id, status=True).select_related("state", "country").first()
        else:
            c = City.objects.filter(pk=city_id, status=True).select_related("state", "country").first()
        if not c:
            return None, None
        city_dto = CityDto(id=int(c.id), title=c.title, state_id=int(c.state_id), state_title=c.state_name)
        state = c.state
        state_dto = StateDto(id=int(state.id), title=state.title) if state else None
        return city_dto, state_dto

