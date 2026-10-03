from django.shortcuts import get_object_or_404
from .models import VendorProfile, VendorBankDetail


class VendorService:

    # --- Vendor Profile Services ---
    @staticmethod
    def create_vendor_profile(user, data: dict) -> VendorProfile:
        return VendorProfile.objects.create(user=user, **data)

    @staticmethod
    def get_vendor_profile_by_user(user) -> VendorProfile:
        return get_object_or_404(VendorProfile.objects.select_related('bank_detail'), user=user)

    @staticmethod
    def get_all_vendors() -> list[VendorProfile]:
        return VendorProfile.objects.filter(is_active=True,
                                            verification_status=VendorProfile.VerificationStatus.APPROVED).select_related(
            'bank_detail')

    @staticmethod
    def update_vendor_profile(user, data: dict) -> VendorProfile:
        profile = get_object_or_404(VendorProfile, user=user)
        for attr, value in data.items():
            if value is not None:
                setattr(profile, attr, value)
        profile.save()
        return profile

    # --- Vendor Bank Details Services ---
    @staticmethod
    def create_or_update_bank_detail(user, data: dict) -> VendorBankDetail:
        profile = get_object_or_404(VendorProfile, user=user)
        bank_detail, created = VendorBankDetail.objects.update_or_create(
            vendor=profile,
            defaults=data
        )
        return bank_detail