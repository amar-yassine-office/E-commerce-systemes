from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import SupportTicket, ReturnRequest


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'customer', 'assigned_agent', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('subject', 'description', 'customer__username', 'customer__email')
    list_editable = ('status', 'priority', 'assigned_agent')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('معلومات التذكرة', {
            'fields': ('subject', 'description', 'customer')
        }),
        ('الحالة والإسناد', {
            'fields': ('assigned_agent', 'status', 'priority')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'customer', 'status', 'processed_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'reason', 'customer__username', 'customer__email')
    list_editable = ('status', 'processed_by')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('تفاصيل الإرجاع', {
            'fields': ('customer', 'order_id', 'reason')
        }),
        ('المعالجة والإدارة', {
            'fields': ('status', 'processed_by')
        }),
        ('التاريخ', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )