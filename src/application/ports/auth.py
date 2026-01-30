from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class TokenPair:
    access: str
    refresh: str


class UserRepositoryPort(Protocol):
    def get_or_create_user_id_by_phone(self, *, phone: str) -> tuple[int, bool]: ...
    def get_user_by_id(self, *, user_id: int) -> dict: ...
    def update_user(self, *, user_id: int, data: dict) -> dict: ...
    def set_user_interested_platforms(self, *, user_id: int, platform_ids: list[int]) -> None: ...


class TokenProviderPort(Protocol):
    def issue_tokens_for_user_id(self, *, user_id: int) -> TokenPair: ...
    def refresh_tokens(self, *, refresh: str) -> TokenPair: ...

