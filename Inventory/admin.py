from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Warehouse, StockItem, StockMovement


class StockMovementInline(admin.TabularInline):
    model = StockMovement
    extra = 0
    readonly_fields = ('movement_type', 'quantity_changed', 'reason', 'performed_by', 'created_at')
    can_delete = False


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code', 'address')
    list_editable = ('is_active',)


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'warehouse', 'quantity', 'reserved_quantity', 'low_stock_threshold', 'updated_at')
    list_filter = ('warehouse', 'updated_at')
    search_fields = ('product__title', 'warehouse__name')
    list_editable = ('quantity', 'reserved_quantity', 'low_stock_threshold')
    readonly_fields = ('updated_at',)
    inlines = [StockMovementInline]

    fieldsets = (
        ('Location & Product', {
            'fields': ('warehouse', 'product')
        }),
        ('Inventory Levels', {
            'fields': ('quantity', 'reserved_quantity', 'low_stock_threshold')
        }),
        ('Timestamp', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('id', 'stock_item', 'movement_type', 'quantity_changed', 'performed_by', 'created_at')
    list_filter = ('movement_type', 'created_at')
    search_fields = ('stock_item__product__title', 'reason', 'performed_by__username')
    readonly_fields = ('stock_item', 'movement_type', 'quantity_changed', 'reason', 'performed_by', 'created_at')