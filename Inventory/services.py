from django.shortcuts import get_object_or_404
from .models import Warehouse, StockItem, StockMovement
from Catalog.models import Product


class InventoryService:

    # --- Warehouse Services ---
    @staticmethod
    def create_warehouse(data: dict) -> Warehouse:
        return Warehouse.objects.create(**data)

    @staticmethod
    def get_all_warehouses() -> list[Warehouse]:
        return Warehouse.objects.filter(is_active=True)

    # --- Stock Item Services ---
    @staticmethod
    def create_stock_item(data: dict) -> StockItem:
        warehouse = get_object_or_404(Warehouse, id=data.pop('warehouse_id'))
        product = get_object_or_404(Product, id=data.pop('product_id'))
        return StockItem.objects.create(warehouse=warehouse, product=product, **data)

    @staticmethod
    def get_warehouse_stock(warehouse_id: int) -> list[StockItem]:
        return StockItem.objects.filter(warehouse_id=warehouse_id).select_related('product')

    # --- Stock Movement Services ---
    @staticmethod
    def record_movement(user, data: dict) -> StockMovement:
        stock_item_id = data.pop('stock_item_id')
        quantity_changed = data.get('quantity_changed')

        stock_item = get_object_or_404(StockItem, id=stock_item_id)

        # تحديث الكمية الفعلية في المخزون تلقائياً بناءً على الحركة
        stock_item.quantity += quantity_changed
        if stock_item.quantity < 0:
            stock_item.quantity = 0  # لمنع نزول الكمية بالسالب
        stock_item.save()

        # إنشاء سجل الحركة
        movement = StockMovement.objects.create(
            stock_item=stock_item,
            performed_by=user,
            **data
        )
        return movement