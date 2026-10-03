from .models import StockItem, StockMovement
from .tasks import check_low_stock_task

class InventoryService:

    @staticmethod
    def adjust_stock(stock_item, quantity_change, movement_type, performed_by, reason=""):
        """
        Adjusts stock item quantity, creates a movement log, and triggers a low-stock check task in the background.
        """
        # Update stock item quantity
        stock_item.quantity += quantity_change
        stock_item.save()

        # Create audit movement log
        movement = StockMovement.objects.create(
            stock_item=stock_item,
            movement_type=movement_type,
            quantity_changed=quantity_change,
            reason=reason,
            performed_by=performed_by
        )

        # Trigger Celery background task to check if stock is now low
        check_low_stock_task.delay(stock_item.id)

        return movement

    # the delete of the cache when the data macke update

    from cache import RedisCacheManager
    from .models import Warehouse, StockItem, StockMovement
    from .tasks import send_low_stock_alert_task

    class InventoryService:

        @staticmethod
        def get_warehouses():
            warehouses = RedisCacheManager.get_inventory_warehouses()

            if warehouses is not None:
                return warehouses

            warehouses = list(Warehouse.objects.filter(is_active=True).values('id', 'name', 'code', 'address'))

            RedisCacheManager.set_inventory_warehouses(warehouses, timeout=60 * 30)
            return warehouses

        @staticmethod
        def create_warehouse(name, code, address, is_active=True):
            warehouse = Warehouse.objects.create(
                name=name,
                code=code,
                address=address,
                is_active=is_active
            )

            RedisCacheManager.clear_inventory_warehouses()
            return warehouse

        @staticmethod
        def adjust_stock(stock_item_id, quantity_change, movement_type, performed_by=None, reason=None):
            try:
                stock_item = StockItem.objects.select_related('product', 'warehouse').get(id=stock_item_id)
                stock_item.quantity += quantity_change
                stock_item.save()

                movement = StockMovement.objects.create(
                    stock_item=stock_item,
                    movement_type=movement_type,
                    quantity_changed=quantity_change,
                    reason=reason,
                    performed_by=performed_by
                )

                if stock_item.quantity <= stock_item.low_stock_threshold:
                    send_low_stock_alert_task.delay(stock_item.id)

                return movement
            except StockItem.DoesNotExist:
                return None