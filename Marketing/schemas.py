from ninja import Schema
from decimal import Decimal
from datetime import datetime
from typing import Optional, List

# --- Coupon Schemas ---
class CouponCreateSchema(Schema):
    code: str
    discount_type: str
    discount_value: Decimal
    min_purchase_amount: Optional[Decimal] = None
    usage_limit: Optional[int] = 100
    applicable_product_ids: Optional[List[int]] = []
    applicable_category_ids: Optional[List[int]] = []
    valid_from: datetime
    valid_to: datetime
    is_active: Optional[bool] = True

class CouponOutSchema(Schema):
    id: int
    code: str
    discount_type: str
    discount_value: Decimal
    min_purchase_amount: Optional[Decimal] = None
    usage_limit: int
    used_count: int
    valid_from: datetime
    valid_to: datetime
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Promotion Banner Schemas ---
class PromotionBannerCreateSchema(Schema):
    title: str
    image: str
    target_url: Optional[str] = None
    position: Optional[str] = 'hero'
    start_date: datetime
    end_date: datetime
    is_active: Optional[bool] = True

class PromotionBannerOutSchema(Schema):
    id: int
    title: str
    image: str
    target_url: Optional[str] = None
    position: str
    is_active: bool
    start_date: datetime
    end_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

# --- Newsletter Subscriber Schemas ---
class NewsletterSubscriberCreateSchema(Schema):
    email: str

class NewsletterSubscriberOutSchema(Schema):
    id: int
    email: str
    is_subscribed: bool
    joined_at: datetime

    class Config:
        from_attributes = True