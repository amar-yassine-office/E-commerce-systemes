from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'percentage', 'Percentage (%)'
        FIXED = 'fixed', 'Fixed Amount'

    code = models.CharField(max_length=50, unique=True, verbose_name="Coupon Code")
    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
        default=DiscountType.PERCENTAGE,
        verbose_name="Discount Type"
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Discount Value")
    min_purchase_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Minimum Purchase Amount"
    )
    usage_limit = models.PositiveIntegerField(default=100, verbose_name="Total Usage Limit")
    used_count = models.PositiveIntegerField(default=0, verbose_name="Used Count")

    # Relationships with the Catalog app (Products & Categories)
    applicable_products = models.ManyToManyField(
        'Catalog.Product',
        blank=True,
        related_name='coupons',
        verbose_name="Applicable Products"
    )
    applicable_categories = models.ManyToManyField(
        'Catalog.Category',
        blank=True,
        related_name='coupons',
        verbose_name="Applicable Categories"
    )

    valid_from = models.DateTimeField(verbose_name="Valid From")
    valid_to = models.DateTimeField(verbose_name="Valid To")
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return f"{self.code} ({self.discount_value} {self.get_discount_type_display()})"


class PromotionBanner(models.Model):
    class BannerPosition(models.TextChoices):
        HERO = 'hero', 'Homepage Hero Slider'
        SIDEBAR = 'sidebar', 'Sidebar Banner'
        FOOTER = 'footer', 'Footer Banner'

    title = models.CharField(max_length=255, verbose_name="Banner Title")
    image = models.ImageField(upload_to='marketing/banners/', verbose_name="Banner Image")
    target_url = models.URLField(blank=True, null=True, verbose_name="Target URL")
    position = models.CharField(
        max_length=30,
        choices=BannerPosition.choices,
        default=BannerPosition.HERO,
        verbose_name="Display Position"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")
    start_date = models.DateTimeField(verbose_name="Start Date")
    end_date = models.DateTimeField(verbose_name="End Date")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Promotion Banner"
        verbose_name_plural = "Promotion Banners"

    def __str__(self):
        return f"{self.title} ({self.get_position_display()})"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Subscriber Email")
    is_subscribed = models.BooleanField(default=True, verbose_name="Is Subscribed?")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Joined At")

    class Meta:
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"

    def __str__(self):
        return self.email