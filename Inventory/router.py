from ninja import Router
from typing import List
from ninja_jwt.authentication import JWTAuth
from .schemas import (
    WarehouseCreateSchema, WarehouseOutSchema,
    StockItemCreateSchema, StockItemOutSchema,
    StockMovementCreateSchema, StockMovementOutSchema
)
from .services import InventoryService

router = Router(tags=["Inventory & Warehouses"])

# --- Warehouse Endpoints ---
@router.post("/warehouses/", response=WarehouseOutSchema, auth=JWTAuth())
def create_warehouse(request, payload: WarehouseCreateSchema):
    return InventoryService.create_warehouse(payload.dict())

@router.get("/warehouses/", response=List[WarehouseOutSchema], auth=JWTAuth())
def list_warehouses(request):
    return InventoryService.get_all_warehouses()

# --- Stock Item Endpoints ---
@router.post("/stock-items/", response=StockItemOutSchema, auth=JWTAuth())
def create_stock_item(request, payload: StockItemCreateSchema):
    return InventoryService.create_stock_item(payload.dict())

@router.get("/warehouses/{warehouse_id}/stock/", response=List[StockItemOutSchema], auth=JWTAuth())
def list_warehouse_stock(request, warehouse_id: int):
    return InventoryService.get_warehouse_stock(warehouse_id)

# --- Stock Movement Endpoints ---
@router.post("/movements/", response=StockMovementOutSchema, auth=JWTAuth())
def record_movement(request, payload: StockMovementCreateSchema):
    return InventoryService.record_movement(request.auth, payload.dict())