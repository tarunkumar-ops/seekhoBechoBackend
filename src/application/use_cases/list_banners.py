from src.application.ports.banner import BannerRepositoryPort, BannerDto


class ListBannersUseCase:
    def __init__(self, *, banner_repo: BannerRepositoryPort) -> None:
        self._banner_repo = banner_repo

    def execute(self, *, placement: str, platform: str) -> list[BannerDto]:
        return self._banner_repo.list_active_banners(placement=placement, platform=platform)

