from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Invoice, PaymentTransaction, VendorPayout


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'customer', 'total_amount', 'tax_amount', 'status', 'issued_at')
    list_filter = ('status', 'issued_at')
    search_fields = ('order_id', 'customer__username', 'customer__email')
    list_editable = ('status',)
    readonly_fields = ('issued_at', 'updated_at')

    fieldsets = (
        ('معلومات الفاتورة', {
            'fields': ('customer', 'order_id', 'total_amount', 'tax_amount')
        }),
        ('الحالة', {
            'fields': ('status',)
        }),
        ('التواريخ', {
            'fields': ('issued_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'invoice', 'gateway', 'amount', 'status', 'created_at')
    list_filter = ('gateway', 'status', 'created_at')
    search_fields = ('transaction_id', 'invoice__id')
    list_editable = ('status',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('تفاصيل المعاملة والفاتورة المرتبطة', {
            'fields': ('invoice', 'gateway', 'transaction_id', 'amount')
        }),
        ('الحالة والتاريخ', {
            'fields': ('status', 'created_at')
        }),
    )


@admin.register(VendorPayout)
class VendorPayoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'amount', 'commission_deducted', 'net_amount', 'status', 'processed_by',
                    'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('vendor__username', 'vendor__email')
    list_editable = ('status', 'processed_by')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('تفاصيل الأرباح والبائع', {
            'fields': ('vendor', 'amount', 'commission_deducted', 'net_amount')
        }),
        ('المعالجة والحالة', {
            'fields': ('status', 'processed_by', 'paid_at')
        }),
        ('التاريخ', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )