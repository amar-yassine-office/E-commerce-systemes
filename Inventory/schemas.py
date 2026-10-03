from ninja import Schema
from datetime import datetime
from typing import Optional, List

# --- Warehouse Schemas ---
class WarehouseCreateSchema(Schema):
    name: str
    code: str
    address: str
    is_active: Optional[bool] = True

class WarehouseOutSchema(Schema):
    id: int
    name: str
    code: str
    address: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Stock Item Schemas ---
class StockItemCreateSchema(Schema):
    warehouse_id: int
    product_id: int
    quantity: Optional[int] = 0
    low_stock_threshold: Optional[int] = 5

class StockItemUpdateSchema(Schema):
    quantity: Optional[int] = None
    reserved_quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None

class StockItemOutSchema(Schema):
    id: int
    warehouse_id: int
    product_id: int
    quantity: int
    reserved_quantity: int
    low_stock_threshold: int
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Stock Movement Schemas ---
class StockMovementCreateSchema(Schema):
    stock_item_id: int
    movement_type: str
    quantity_changed: int
    reason: Optional[str] = None

class StockMovementOutSchema(Schema):
    id: int
    stock_item_id: int
    movement_type: str
    quantity_changed: int
    reason: Optional[str] = None
    performed_by_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True