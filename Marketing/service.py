from .models import Coupon, PromotionBanner, NewsletterSubscriber
from .tasks import send_newsletter_welcome_task


class MarketingService:

    @staticmethod
    def subscribe_to_newsletter(email):
        """
        Subscribes a new email to the newsletter and triggers a welcome email task.
        """
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={'is_subscribed': True}
        )

        if created or not subscriber.is_subscribed:
            subscriber.is_subscribed = True
            subscriber.save()

            # Trigger Celery background task
            send_newsletter_welcome_task.delay(subscriber.id)

        return subscriber

    @staticmethod
    def create_coupon(code, discount_type, discount_value, valid_from, valid_to, usage_limit=100,
                      min_purchase_amount=None):
        """
        Creates a new marketing coupon.
        """
        coupon = Coupon.objects.create(
            code=code,
            discount_type=discount_type,
            discount_value=discount_value,
            valid_from=valid_from,
            valid_to=valid_to,
            usage_limit=usage_limit,
            min_purchase_amount=min_purchase_amount,
            is_active=True
        )
        return coupon

    # the delete od the cache function when  the data macke update

    from django.utils import timezone
    from cache import RedisCacheManager
    from .models import Coupon, PromotionBanner, NewsletterSubscriber
    from .tasks import send_newsletter_welcome_task

    class MarketingService:

        @staticmethod
        def get_active_banners():
            banners = RedisCacheManager.get_marketing_banners()

            if banners is not None:
                return banners

            now = timezone.now()
            banners = list(PromotionBanner.objects.filter(
                is_active=True,
                start_date__lte=now,
                end_date__gte=now
            ).values('id', 'title', 'image', 'target_url', 'position'))

            RedisCacheManager.set_marketing_banners(banners, timeout=60 * 60)
            return banners

        @staticmethod
        def create_promotion_banner(title, image, start_date, end_date, target_url=None,
                                    position=PromotionBanner.BannerPosition.HERO, is_active=True):
            banner = PromotionBanner.objects.create(
                title=title,
                image=image,
                target_url=target_url,
                position=position,
                start_date=start_date,
                end_date=end_date,
                is_active=is_active
            )

            RedisCacheManager.clear_marketing_banners()
            return banner

        @staticmethod
        def get_coupon_by_code(code):
            coupon_data = RedisCacheManager.get_marketing_coupon(code)

            if coupon_data is not None:
                return coupon_data

            try:
                coupon = Coupon.objects.get(code=code, is_active=True)
                coupon_data = {
                    'id': coupon.id,
                    'code': coupon.code,
                    'discount_type': coupon.discount_type,
                    'discount_value': float(coupon.discount_value),
                    'min_purchase_amount': float(coupon.min_purchase_amount) if coupon.min_purchase_amount else 0.0,
                    'usage_limit': coupon.usage_limit,
                    'used_count': coupon.used_count
                }
                RedisCacheManager.set_marketing_coupon(code, coupon_data, timeout=60 * 15)
                return coupon_data
            except Coupon.DoesNotExist:
                return None

        @staticmethod
        def subscribe_to_newsletter(email):
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'is_subscribed': True}
            )

            if created or not subscriber.is_subscribed:
                subscriber.is_subscribed = True
                subscriber.save()
                send_newsletter_welcome_task.delay(subscriber.id)

            return subscriber