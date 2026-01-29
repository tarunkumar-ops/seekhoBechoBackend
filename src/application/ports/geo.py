from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class StateDto:
    id: int
    title: str


@dataclass(frozen=True)
class CityDto:
    id: int
    title: str
    state_id: int | None = None
    state_title: str | None = None


class GeoRepositoryPort(Protocol):
    def list_states(self, *, country_iso2: str) -> list[StateDto]: ...

    def list_cities_by_state(self, *, state_id: int) -> list[CityDto]: ...
    def list_cities_by_query(self, *, q: str) -> list[CityDto]: ...
    def get_city_with_state(self, *, city_id: int) -> tuple[CityDto | None, StateDto | None]: ...
    def get_state_by_id(self, *, state_id: int) -> StateDto | None: ...

