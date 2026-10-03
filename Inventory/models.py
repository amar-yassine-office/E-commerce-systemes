from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Warehouse(models.Model):
    name = models.CharField(max_length=255, verbose_name="Warehouse Name")
    code = models.CharField(max_length=50, unique=True, verbose_name="Warehouse Code")
    address = models.TextField(verbose_name="Warehouse Address")
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"

    def __str__(self):
        return f"{self.name} ({self.code})"


class StockItem(models.Model):
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='stock_items',
        verbose_name="Warehouse"
    )
    # Relationship with the Product model from the Catalog app
    product = models.ForeignKey(
        'Catalog.Product',
        on_delete=models.CASCADE,
        related_name='stock_items',
        verbose_name="Product"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Available Quantity")
    reserved_quantity = models.PositiveIntegerField(default=0, verbose_name="Reserved Quantity")
    low_stock_threshold = models.PositiveIntegerField(default=5, verbose_name="Low Stock Threshold")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        verbose_name = "Stock Item"
        verbose_name_plural = "Stock Items"
        unique_together = ('warehouse', 'product')

    def __str__(self):
        return f"{self.product.title} @ {self.warehouse.name} (Stock: {self.quantity})"


class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        RESTOCK = 'restock', 'Restock / Purchase'
        SALE = 'sale', 'Order Sale'
        RETURN = 'return', 'Customer Return'
        ADJUSTMENT = 'adjustment', 'Manual Adjustment'

    stock_item = models.ForeignKey(
        StockItem,
        on_delete=models.CASCADE,
        related_name='movements',
        verbose_name="Stock Item"
    )
    movement_type = models.CharField(
        max_length=30,
        choices=MovementType.choices,
        verbose_name="Movement Type"
    )
    quantity_changed = models.IntegerField(verbose_name="Quantity Changed (+/-)")
    reason = models.TextField(blank=True, null=True, verbose_name="Reason / Notes")
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stock_movements',
        verbose_name="Performed By"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Movement Date")

    class Meta:
        verbose_name = "Stock Movement"
        verbose_name_plural = "Stock Movements"

    def __str__(self):
        return f"{self.get_movement_type_display()} : {self.quantity_changed} ({self.stock_item.product.title})"