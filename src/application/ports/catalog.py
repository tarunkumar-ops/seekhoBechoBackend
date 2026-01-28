from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class CategoryDto:
    id: int
    title: str
    description: str | None
    cat_img: str | None


@dataclass(frozen=True)
class ProductDto:
    id: int
    product_code: str
    product_name: str
    selling_price: str
    offer_price: str | None


@dataclass(frozen=True)
class SubscriptionDto:
    id: int
    plan_code: str
    plan_name: str
    total_amount: str


class CatalogRepositoryPort(Protocol):
    def list_categories(self) -> list[CategoryDto]: ...

    def list_products_by_category(self, *, category_id: int) -> list[ProductDto]: ...

    def get_product(self, *, product_id: int) -> ProductDto | None: ...

    def list_subscriptions(self) -> list[SubscriptionDto]: ...

