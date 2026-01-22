from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class TokenPair:
    access: str
    refresh: str


class UserRepositoryPort(Protocol):
    def get_or_create_user_id_by_phone(self, *, phone: str) -> int: ...


class TokenProviderPort(Protocol):
    def issue_tokens_for_user_id(self, *, user_id: int) -> TokenPair: ...

