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


class GeoRepositoryPort(Protocol):
    def list_states(self, *, country_iso2: str) -> list[StateDto]: ...

    def list_cities_by_state(self, *, state_id: int) -> list[CityDto]: ...

