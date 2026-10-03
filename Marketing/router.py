from ninja import Router
from typing import List
from ninja_jwt.authentication import JWTAuth
from .schemas import (
    CouponCreateSchema, CouponOutSchema,
    PromotionBannerCreateSchema, PromotionBannerOutSchema,
    NewsletterSubscriberCreateSchema, NewsletterSubscriberOutSchema
)
from .services import MarketingService

router = Router(tags=["Marketing & Promotions"])

# --- Coupons Endpoints ---
@router.post("/coupons/", response=CouponOutSchema, auth=JWTAuth())
def create_coupon(request, payload: CouponCreateSchema):
    return MarketingService.create_coupon(payload.dict())

@router.get("/coupons/", response=List[CouponOutSchema], auth=JWTAuth())
def list_coupons(request):
    return MarketingService.get_all_coupons()

# --- Banners Endpoints ---
@router.post("/banners/", response=PromotionBannerOutSchema, auth=JWTAuth())
def create_banner(request, payload: PromotionBannerCreateSchema):
    return MarketingService.create_banner(payload.dict())

@router.get("/banners/", response=List[PromotionBannerOutSchema])
def list_active_banners(request):
    return MarketingService.get_active_banners()

# --- Newsletter Endpoints ---
@router.post("/newsletter/subscribe/", response=NewsletterSubscriberOutSchema)
def subscribe_newsletter(request, payload: NewsletterSubscriberCreateSchema):
    return MarketingService.subscribe_newsletter(payload.dict())