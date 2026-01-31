from src.application.ports.media import MediaRepositoryPort, MediaDto
from src.infrastructure.persistence.models import SbMedia


class DjangoMediaRepository(MediaRepositoryPort):
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
        m = SbMedia.objects.create(
            media_type=media_type,
            media_url=media_url,
            poster_url=poster_url,
            width=width,
            height=height,
            duration=duration,
        )
        return MediaDto(
            id=str(m.id),
            media_type=m.media_type,
            media_url=m.media_url,
            poster_url=m.poster_url,
            width=m.width,
            height=m.height,
            duration=m.duration,
        )

