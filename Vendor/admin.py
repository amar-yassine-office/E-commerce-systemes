from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import VendorProfile, VendorBankDetail


class VendorBankDetailInline(admin.StackedInline):
    model = VendorBankDetail
    can_delete = False
    extra = 0


@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'verification_status', 'commission_rate', 'is_active', 'created_at')
    list_filter = ('verification_status', 'is_active', 'created_at')
    search_fields = ('store_name', 'user__username', 'user__email')
    list_editable = ('verification_status', 'commission_rate', 'is_active')
    prepopulated_fields = {'store_slug': ('store_name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [VendorBankDetailInline]

    fieldsets = (
        ('Store Information', {
            'fields': ('user', 'store_name', 'store_slug', 'store_description', 'logo', 'banner')
        }),
        ('Business & Governance', {
            'fields': ('verification_status', 'commission_rate', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VendorBankDetail)
class VendorBankDetailAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'bank_name', 'account_holder_name', 'account_number', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('vendor__store_name', 'bank_name', 'account_holder_name')
    list_editable = ('is_verified',)
    readonly_fields = ('created_at',)