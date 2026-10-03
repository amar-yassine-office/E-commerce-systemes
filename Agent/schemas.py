from ninja import Schema
from datetime import datetime
from typing import Optional

# --- Support Ticket Schemas ---
class SupportTicketCreateSchema(Schema):
    subject: str
    description: str
    priority: Optional[str] = 'medium'

class SupportTicketOutSchema(Schema):
    id: int
    customer_id: int
    assigned_agent_id: Optional[int] = None
    subject: str
    description: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SupportTicketUpdateSchema(Schema):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_agent_id: Optional[int] = None

# --- Return Request Schemas ---
class ReturnRequestCreateSchema(Schema):
    order_id: int
    reason: str

class ReturnRequestOutSchema(Schema):
    id: int
    customer_id: int
    order_id: int
    reason: str
    status: str
    processed_by_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ReturnRequestUpdateSchema(Schema):
    status: str