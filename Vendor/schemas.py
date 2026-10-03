from ninja import Schema
from decimal import Decimal
from datetime import datetime
from typing import Optional

# --- Vendor Bank Detail Schemas ---
class VendorBankDetailCreateSchema(Schema):
    bank_name: str
    account_holder_name: str
    account_number: str
    swift_code: Optional[str] = None

class VendorBankDetailOutSchema(Schema):
    id: int
    bank_name: str
    account_holder_name: str
    account_number: str
    swift_code: Optional[str] = None
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Vendor Profile Schemas ---
class VendorProfileCreateSchema(Schema):
    store_name: str
    store_slug: str
    store_description: Optional[str] = None
    logo: Optional[str] = None
    banner: Optional[str] = None

class VendorProfileUpdateSchema(Schema):
    store_description: Optional[str] = None
    logo: Optional[str] = None
    banner: Optional[str] = None

class VendorProfileOutSchema(Schema):
    id: int
    user_id: int
    store_name: str
    store_slug: str
    store_description: Optional[str] = None
    logo: Optional[str] = None
    banner: Optional[str] = None
    verification_status: str
    commission_rate: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime
    bank_detail: Optional[VendorBankDetailOutSchema] = None

    class Config:
        from_attributes = True