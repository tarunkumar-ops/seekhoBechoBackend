from dataclasses import dataclass

from src.infrastructure.storage.r2_service import R2Service


@dataclass
class PresignResult:
    upload_url: str
    key: str
    public_url: str


class PresignMediaUseCase:
    def __init__(self, *, r2_service: R2Service, expires: int = 300) -> None:
        self._r2 = r2_service
        self._expires = expires

    def execute(self, *, file_name: str, content_type: str, media_type: str) -> PresignResult:
        # build key namespaced by media type and uuid-ish name
        from uuid import uuid4

        key = f"media/{media_type}/{uuid4().hex}/{file_name}"
        upload_url = self._r2.generate_presigned_put(key=key, content_type=content_type, expires=self._expires)
        public_url = self._r2.public_url_for_key(key)
        return PresignResult(upload_url=upload_url, key=key, public_url=public_url)

