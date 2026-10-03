from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Coupon, PromotionBanner, NewsletterSubscriber


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'usage_limit', 'used_count', 'valid_from', 'valid_to',
                    'is_active')
    list_filter = ('discount_type', 'is_active', 'valid_from', 'valid_to')
    search_fields = ('code',)
    list_editable = ('is_active', 'discount_value')
    filter_horizontal = ('applicable_products', 'applicable_categories')

    fieldsets = (
        ('Coupon Details', {
            'fields': ('code', 'discount_type', 'discount_value', 'min_purchase_amount')
        }),
        ('Usage Limits', {
            'fields': ('usage_limit', 'used_count')
        }),
        ('Applicable Targets', {
            'fields': ('applicable_products', 'applicable_categories')
        }),
        ('Validity & Status', {
            'fields': ('valid_from', 'valid_to', 'is_active')
        }),
    )


@admin.register(PromotionBanner)
class PromotionBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'is_active', 'start_date', 'end_date')
    list_filter = ('position', 'is_active', 'start_date')
    search_fields = ('title',)
    list_editable = ('is_active',)

    fieldsets = (
        ('Banner Information', {
            'fields': ('title', 'image', 'target_url', 'position')
        }),
        ('Schedule & Status', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
    )


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_subscribed', 'joined_at')
    list_filter = ('is_subscribed', 'joined_at')
    search_fields = ('email',)
    list_editable = ('is_subscribed',)