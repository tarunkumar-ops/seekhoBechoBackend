from typing import List

from src.application.ports.catalog import CatalogRepositoryPort, CategoryDto, ProductDto, SubscriptionDto
from src.infrastructure.persistence.models import SbCategory, SbProduct, SbSubscription


class DjangoCatalogRepository(CatalogRepositoryPort):
    def list_categories(self) -> List[CategoryDto]:
        qs = SbCategory.objects.filter(status=True).order_by("title")
        return [CategoryDto(id=int(c.id), title=c.title, description=c.description, cat_img=c.cat_img) for c in qs]

    def list_products_by_category(self, *, category_id: int) -> List[ProductDto]:
        qs = SbProduct.objects.filter(cat_id=category_id, status=True).order_by("product_name")
        return [ProductDto(id=int(p.id), product_code=p.product_code, product_name=p.product_name, selling_price=str(p.selling_price), offer_price=(str(p.offer_price) if p.offer_price is not None else None)) for p in qs]

    def get_product(self, *, product_id: int) -> ProductDto | None:
        p = SbProduct.objects.filter(pk=product_id, status=True).first()
        if not p:
            return None
        return ProductDto(id=int(p.id), product_code=p.product_code, product_name=p.product_name, selling_price=str(p.selling_price), offer_price=(str(p.offer_price) if p.offer_price is not None else None))

    def list_subscriptions(self) -> List[SubscriptionDto]:
        qs = SbSubscription.objects.filter(status=True).order_by("-is_default", "plan_name")
        return [SubscriptionDto(id=int(s.id), plan_code=s.plan_code, plan_name=s.plan_name, total_amount=str(s.total_amount)) for s in qs]

