from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class OccupationDto:
    id: int
    title: str


@dataclass(frozen=True)
class PlatformDto:
    id: int
    title: str


class ConfigRepositoryPort(Protocol):
    def list_occupations(self) -> list[OccupationDto]: ...

    def list_interested_platforms(self) -> list[PlatformDto]: ...

