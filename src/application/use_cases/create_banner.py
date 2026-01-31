from datetime import datetime
from src.application.ports.banner import BannerRepositoryPort, BannerDto
from src.shared.exceptions import ValidationError


class CreateBannerUseCase:
    def __init__(self, *, banner_repo: BannerRepositoryPort) -> None:
        self._banner_repo = banner_repo

    def execute(
        self,
        *,
        title: str | None,
        media_id: str,
        placement: str,
        platform: str,
        target_type: str,
        target_value: str | None = None,
        start_at: str | None = None,
        end_at: str | None = None,
        priority: int = 0,
        is_active: bool = True,
    ) -> BannerDto:
        # basic validation
        if not placement or not platform:
            raise ValidationError("placement and platform are required")
        if target_type == "external" and not target_value:
            raise ValidationError("target_value is required for external target_type")
        if start_at and end_at:
            try:
                sa = datetime.fromisoformat(start_at)
                ea = datetime.fromisoformat(end_at)
            except Exception:
                raise ValidationError("start_at and end_at must be ISO datetimes")
            if sa >= ea:
                raise ValidationError("start_at must be before end_at")

        banner = self._banner_repo.create_banner(
            title=title,
            media_id=media_id,
            placement=placement,
            platform=platform,
            target_type=target_type,
            target_value=target_value,
            start_at=start_at,
            end_at=end_at,
            priority=priority,
            is_active=is_active,
        )
        return banner

