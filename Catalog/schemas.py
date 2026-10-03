from ninja import Schema
from decimal import Decimal
from datetime import datetime
from typing import Optional, List

# --- Category Schemas ---
class CategoryCreateSchema(Schema):
    name: str
    slug: str
    parent_id: Optional[int] = None
    is_active: Optional[bool] = True

class CategoryOutSchema(Schema):
    id: int
    name: str
    slug: str
    parent_id: Optional[int] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Product Attribute Schemas ---
class ProductAttributeCreateSchema(Schema):
    name: str
    value: str

class ProductAttributeOutSchema(Schema):
    id: int
    name: str
    value: str

    class Config:
        from_attributes = True

# --- Product Image Schemas ---
class ProductImageCreateSchema(Schema):
    image: str  # أو رابط الصورة
    is_feature: Optional[bool] = False

class ProductImageOutSchema(Schema):
    id: int
    image: str
    is_feature: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Product Schemas ---
class ProductCreateSchema(Schema):
    category_id: Optional[int] = None
    title: str
    slug: str
    description: str
    price: Decimal
    compare_at_price: Optional[Decimal] = None
    is_active: Optional[bool] = True
    attributes: Optional[List[ProductAttributeCreateSchema]] = []

class ProductOutSchema(Schema):
    id: int
    vendor_id: int
    category_id: Optional[int] = None
    title: str
    slug: str
    description: str
    price: Decimal
    compare_at_price: Optional[Decimal] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    attributes: List[ProductAttributeOutSchema] = []
    images: List[ProductImageOutSchema] = []

    class Config:
        from_attributes = True