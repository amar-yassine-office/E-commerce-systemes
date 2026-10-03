from ninja import Schema
from decimal import Decimal
from datetime import datetime
from typing import Optional, List

# --- Invoice Schemas ---
class InvoiceCreateSchema(Schema):
    customer_id: int
    order_id: int
    total_amount: Decimal
    tax_amount: Decimal = Decimal('0.00')
    status: Optional[str] = 'pending'

class InvoiceOutSchema(Schema):
    id: int
    customer_id: int
    order_id: int
    total_amount: Decimal
    tax_amount: Decimal
    status: str
    issued_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Payment Transaction Schemas ---
class PaymentTransactionCreateSchema(Schema):
    invoice_id: int
    gateway: str
    transaction_id: str
    amount: Decimal
    status: Optional[str] = 'pending'

class PaymentTransactionOutSchema(Schema):
    id: int
    invoice_id: int
    gateway: str
    transaction_id: str
    amount: Decimal
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Vendor Payout Schemas ---
class VendorPayoutCreateSchema(Schema):
    vendor_id: int
    amount: Decimal
    commission_deducted: Decimal
    net_amount: Decimal
    status: Optional[str] = 'pending'

class VendorPayoutOutSchema(Schema):
    id: int
    vendor_id: int
    amount: Decimal
    commission_deducted: Decimal
    net_amount: Decimal
    status: str
    processed_by_id: Optional[int] = None
    created_at: datetime
    paid_at: Optional[datetime] = None

    class Config:
        from_attributes = True