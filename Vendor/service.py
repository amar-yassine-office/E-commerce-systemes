from django.utils.text import slugify
from .models import VendorProfile, VendorBankDetail
from .tasks import send_vendor_verification_email_task, send_bank_verification_notice_task

class VendorService:

    @staticmethod
    def register_vendor(user, store_name, store_description=None, logo=None, banner=None):
        """
        Registers a new vendor profile, generates a unique store slug, and sets initial status.
        """
        base_slug = slugify(store_name)
        store_slug = base_slug
        counter = 1

        while VendorProfile.objects.filter(store_slug=store_slug).exists():
            store_slug = f"{base_slug}-{counter}"
            counter += 1

        vendor_profile = VendorProfile.objects.create(
            user=user,
            store_name=store_name,
            store_slug=store_slug,
            store_description=store_description,
            logo=logo,
            banner=banner,
            verification_status=VendorProfile.VerificationStatus.PENDING
        )
        return vendor_profile

    @staticmethod
    def update_verification_status(vendor_profile_id, new_status):
        """
        Updates the vendor verification status and triggers a background email task.
        """
        try:
            vendor_profile = VendorProfile.objects.get(id=vendor_profile_id)
            vendor_profile.verification_status = new_status
            vendor_profile.save()

            # Trigger Celery background notification task
            send_vendor_verification_email_task.delay(vendor_profile.id)
            return vendor_profile
        except VendorProfile.DoesNotExist:
            return None

    @staticmethod
    def verify_bank_details(bank_detail_id):
        """
        Verifies vendor bank details and triggers a background notification task.
        """
        try:
            bank_detail = VendorBankDetail.objects.get(id=bank_detail_id)
            bank_detail.is_verified = True
            bank_detail.save()

            # Trigger Celery background notification task
            send_bank_verification_notice_task.delay(bank_detail.id)
            return bank_detail
        except VendorBankDetail.DoesNotExist:
            return None

        # the delete if the cache fucntions when the data macke update

        from django.utils.text import slugify
        from cache import RedisCacheManager
        from .models import VendorProfile, VendorBankDetail
        from .tasks import notify_vendor_approval_task

        class VendorService:

            @staticmethod
            def get_vendor_by_slug(store_slug):
                vendor_data = RedisCacheManager.get_vendor_profile(store_slug)

                if vendor_data is not None:
                    return vendor_data

                try:
                    vendor = VendorProfile.objects.get(store_slug=store_slug,
                                                       verification_status=VendorProfile.VerificationStatus.APPROVED,
                                                       is_active=True)
                    vendor_data = {
                        'id': vendor.id,
                        'store_name': vendor.store_name,
                        'store_slug': vendor.store_slug,
                        'store_description': vendor.store_description,
                        'logo': vendor.logo.url if vendor.logo else None,
                        'banner': vendor.banner.url if vendor.banner else None,
                        'commission_rate': float(vendor.commission_rate)
                    }
                    RedisCacheManager.set_vendor_profile(store_slug, vendor_data, timeout=60 * 30)
                    return vendor_data
                except VendorProfile.DoesNotExist:
                    return None

            @staticmethod
            def create_vendor_profile(user, store_name, store_description=None, logo=None, banner=None):
                base_slug = slugify(store_name)
                store_slug = base_slug
                counter = 1

                while VendorProfile.objects.filter(store_slug=store_slug).exists():
                    store_slug = f"{base_slug}-{counter}"
                    counter += 1

                vendor = VendorProfile.objects.create(
                    user=user,
                    store_name=store_name,
                    store_slug=store_slug,
                    store_description=store_description,
                    logo=logo,
                    banner=banner,
                    verification_status=VendorProfile.VerificationStatus.PENDING
                )

                return vendor

            @staticmethod
            def update_verification_status(vendor_id, new_status):
                try:
                    vendor = VendorProfile.objects.get(id=vendor_id)
                    vendor.verification_status = new_status
                    vendor.save()

                    RedisCacheManager.clear_vendor_profile(vendor.store_slug)
                    notify_vendor_approval_task.delay(vendor.id)
                    return vendor
                except VendorProfile.DoesNotExist:
                    return None