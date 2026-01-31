from src.application.ports.media import MediaRepositoryPort, MediaDto
from src.shared.exceptions import ValidationError


class ConfirmMediaUseCase:
    def __init__(self, *, media_repo: MediaRepositoryPort) -> None:
        self._media_repo = media_repo

    def execute(
        self,
        *,
        media_type: str,
        media_url: str,
        poster_url: str | None = None,
        width: int | None = None,
        height: int | None = None,
        duration: float | None = None,
    ) -> MediaDto:
        media_type = (media_type or "").strip().lower()
        if media_type not in {"image", "video"}:
            raise ValidationError("media_type must be 'image' or 'video'")
        if not media_url:
            raise ValidationError("media_url is required")
        if media_type == "video" and not poster_url:
            raise ValidationError("poster_url is required for video media")

        # Persist media record (no downloads/uploads here)
        media = self._media_repo.create_media(
            media_type=media_type,
            media_url=media_url,
            poster_url=poster_url,
            width=width,
            height=height,
            duration=duration,
        )
        return media

