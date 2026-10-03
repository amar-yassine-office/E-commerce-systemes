from ninja import Router
from typing import List
from ninja_jwt.authentication import JWTAuth
from .schemas import (
    VendorProfileCreateSchema, VendorProfileUpdateSchema, VendorProfileOutSchema,
    VendorBankDetailCreateSchema, VendorBankDetailOutSchema
)
from .services import VendorService

router = Router(tags=["Vendor Management"])

# --- Vendor Profile Endpoints ---
@router.post("/profile/", response=VendorProfileOutSchema, auth=JWTAuth())
def create_profile(request, payload: VendorProfileCreateSchema):
    return VendorService.create_vendor_profile(request.auth, payload.dict())

@router.get("/profile/me/", response=VendorProfileOutSchema, auth=JWTAuth())
def get_my_profile(request):
    return VendorService.get_vendor_profile_by_user(request.auth)

@router.patch("/profile/me/", response=VendorProfileOutSchema, auth=JWTAuth())
def update_my_profile(request, payload: VendorProfileUpdateSchema):
    return VendorService.update_vendor_profile(request.auth, payload.dict())

@router.get("/stores/", response=List[VendorProfileOutSchema])
def list_active_vendors(request):
    return VendorService.get_all_vendors()

# --- Vendor Bank Details Endpoints ---
@router.post("/bank-detail/", response=VendorBankDetailOutSchema, auth=JWTAuth())
def save_bank_detail(request, payload: VendorBankDetailCreateSchema):
    return VendorService.create_or_update_bank_detail(request.auth, payload.dict())