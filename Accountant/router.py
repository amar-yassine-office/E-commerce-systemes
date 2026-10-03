from ninja import Router
from typing import List
from ninja_jwt.authentication import JWTAuth
from .schemas import (
    InvoiceCreateSchema, InvoiceOutSchema,
    PaymentTransactionCreateSchema, PaymentTransactionOutSchema,
    VendorPayoutCreateSchema, VendorPayoutOutSchema
)
from .services import AccountantService

router = Router(tags=["Accountant Management"])

# --- Invoices Endpoints ---
@router.post("/invoices/", response=InvoiceOutSchema, auth=JWTAuth())
def create_invoice(request, payload: InvoiceCreateSchema):
    return AccountantService.create_invoice(payload.dict())

@router.get("/invoices/", response=List[InvoiceOutSchema], auth=JWTAuth())
def list_invoices(request):
    return AccountantService.get_all_invoices()

@router.get("/invoices/{invoice_id}", response=InvoiceOutSchema, auth=JWTAuth())
def get_invoice(request, invoice_id: int):
    return AccountantService.get_invoice_by_id(invoice_id)

# --- Transactions Endpoints ---
@router.post("/transactions/", response=PaymentTransactionOutSchema, auth=JWTAuth())
def create_transaction(request, payload: PaymentTransactionCreateSchema):
    return AccountantService.create_transaction(payload.dict())

@router.get("/invoices/{invoice_id}/transactions/", response=List[PaymentTransactionOutSchema], auth=JWTAuth())
def list_invoice_transactions(request, invoice_id: int):
    return AccountantService.get_invoice_transactions(invoice_id)

# --- Vendor Payouts Endpoints ---
@router.post("/payouts/", response=VendorPayoutOutSchema, auth=JWTAuth())
def create_payout(request, payload: VendorPayoutCreateSchema):
    return AccountantService.create_payout(payload.dict())

@router.post("/payouts/{payout_id}/approve", response=VendorPayoutOutSchema, auth=JWTAuth())
def approve_payout(request, payout_id: int):
    return AccountantService.process_payout(payout_id, request.auth)