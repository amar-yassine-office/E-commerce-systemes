from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import VendorProfile, VendorBankDetail


@shared_task(bind=True, max_retries=3)
def send_vendor_verification_email_task(self, vendor_profile_id):
    """
    Background task to notify a vendor about their store verification status update.
    """
    try:
        vendor_profile = VendorProfile.objects.select_related('user').get(id=vendor_profile_id)
        subject = f"Store Verification Update: {vendor_profile.store_name}"
        message = (
            f"Dear {vendor_profile.user.username},\n\n"
            f"Your store '{vendor_profile.store_name}' verification status has been updated.\n"
            f"Current Status: {vendor_profile.get_verification_status_display()}\n\n"
            f"Best regards,\nPlatform Management"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [vendor_profile.user.email],
            fail_silently=False,
        )
        return f"Verification email sent for vendor store: {vendor_profile.store_name}"
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_bank_verification_notice_task(self, bank_detail_id):
    """
    Background task to notify a vendor when their bank details have been verified.
    """
    try:
        bank_detail = VendorBankDetail.objects.select_related('vendor__user').get(id=bank_detail_id)
        vendor = bank_detail.vendor

        subject = f"Bank Account Verification Notice - {bank_detail.bank_name}"
        message = (
            f"Dear {vendor.user.username},\n\n"
            f"Your bank account details for store '{vendor.store_name}' have been successfully verified.\n"
            f"You are now ready to receive payouts seamlessly.\n\n"
            f"Best regards,\nFinance Team"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [vendor.user.email],
            fail_silently=False,
        )
        return f"Bank verification notice sent for vendor: {vendor.store_name}"
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)