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


class MediaRepositoryPort(Protocol):
    def create_media(
        self,
        *,
        media_type: str,
        media_url: str,
        poster_url: str | None = None,
        width: int | None = None,
        height: int | None = None,
        duration: float | None = None,
    ) -> MediaDto:
        ...

