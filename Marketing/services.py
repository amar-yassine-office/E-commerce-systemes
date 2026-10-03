from django.shortcuts import get_object_or_404
from .models import Coupon, PromotionBanner, NewsletterSubscriber
from Catalog.models import Product, Category


class MarketingService:

    # --- Coupons Services ---
    @staticmethod
    def create_coupon(data: dict) -> Coupon:
        product_ids = data.pop('applicable_product_ids', [])
        category_ids = data.pop('applicable_category_ids', [])

        coupon = Coupon.objects.create(**data)

        if product_ids:
            coupon.applicable_products.set(product_ids)
        if category_ids:
            coupon.applicable_categories.set(category_ids)

        return coupon

    @staticmethod
    def get_all_coupons() -> list[Coupon]:
        return Coupon.objects.all().order_by('-created_at')

    # --- Banners Services ---
    @staticmethod
    def create_banner(data: dict) -> PromotionBanner:
        return PromotionBanner.objects.create(**data)

    @staticmethod
    def get_active_banners() -> list[PromotionBanner]:
        return PromotionBanner.objects.filter(is_active=True)

    # --- Newsletter Services ---
    @staticmethod
    def subscribe_newsletter(data: dict) -> NewsletterSubscriber:
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=data.get('email'),
            defaults={'is_subscribed': True}
        )
        if not created and not subscriber.is_subscribed:
            subscriber.is_subscribed = True
            subscriber.save()
        return subscriber