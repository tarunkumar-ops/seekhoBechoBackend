from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class MediaDto:
    id: str
    media_type: str
    media_url: str
    poster_url: str | None
    width: int | None
    height: int | None
    duration: float | None


@dataclass(frozen=True)
class BannerDto:
    id: str
    title: str | None
    media: MediaDto
    placement: str
    platform: str
    target_type: str
    target_value: str | None
    priority: int


class BannerRepositoryPort(Protocol):
    def list_active_banners(self, *, placement: str, platform: str) -> list[BannerDto]: ...

