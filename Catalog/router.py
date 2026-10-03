from ninja import Router
from typing import List
from ninja_jwt.authentication import JWTAuth
from .schemas import (
    CategoryCreateSchema, CategoryOutSchema,
    ProductCreateSchema, ProductOutSchema
)
from .services import CatalogService

router = Router(tags=["Catalog & Products"])

# --- Categories Endpoints ---
@router.post("/categories/", response=CategoryOutSchema, auth=JWTAuth())
def create_category(request, payload: CategoryCreateSchema):
    return CatalogService.create_category(payload.dict())

@router.get("/categories/", response=List[CategoryOutSchema])
def list_categories(request):
    return CatalogService.get_all_categories()

# --- Products Endpoints ---
@router.post("/products/", response=ProductOutSchema, auth=JWTAuth())
def create_product(request, payload: ProductCreateSchema):
    return CatalogService.create_product(request.auth, payload.dict())

@router.get("/products/", response=List[ProductOutSchema])
def list_products(request):
    return CatalogService.get_all_products()

@router.get("/products/{product_id}", response=ProductOutSchema)
def get_product(request, product_id: int):
    return CatalogService.get_product_by_id(product_id)