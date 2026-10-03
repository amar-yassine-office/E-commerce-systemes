from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Invoice, PaymentTransaction, VendorPayout


@shared_task(bind=True, max_retries=3)
def send_invoice_notification_task(self, invoice_id):
    """
    Background task to send an invoice creation or status update email to the customer.
    """
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        subject = f"Invoice #{invoice.id} for Order #{invoice.order_id}"
        message = (
            f"Hello {invoice.customer.username},\n\n"
            f"Your invoice has been generated successfully with a total amount of: {invoice.total_amount}\n"
            f"Current Status: {invoice.get_status_display()}\n\n"
            f"Thank you for your business!"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [invoice.customer.email],
            fail_silently=False,
        )
        return f"Invoice email sent successfully for Invoice ID: {invoice_id}"
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def verify_payment_transaction_task(self, transaction_id):
    """
    Background task to process or verify a payment transaction asynchronously.
    """
    try:
        transaction = PaymentTransaction.objects.get(id=transaction_id)
        # Add your payment gateway verification logic here (e.g., Stripe/PayPal API call)

        # Example simulation check:
        if transaction.status == PaymentTransaction.PaymentStatus.PENDING:
            transaction.status = PaymentTransaction.PaymentStatus.SUCCESS
            transaction.save()

            # Update corresponding invoice status
            invoice = transaction.invoice
            invoice.status = Invoice.InvoiceStatus.PAID
            invoice.save()

        return f"Transaction #{transaction.transaction_id} verified successfully."
    except Exception as exc:
        raise self.retry(exc=exc, countdown=30)


@shared_task(bind=True, max_retries=3)
def send_vendor_payout_notification_task(self, payout_id):
    """
    Background task to notify the vendor when their payout has been successfully transferred.
    """
    try:
        payout = VendorPayout.objects.get(id=payout_id)
        subject = f"Payout Transferred - Net Amount: {payout.net_amount}"
        message = (
            f"Dear {payout.vendor.username},\n\n"
            f"Your payout request has been processed and transferred successfully.\n"
            f"Net Amount: {payout.net_amount}\n"
            f"Commission Deducted: {payout.commission_deducted}\n\n"
            f"Best regards,\nPlatform Management"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [payout.vendor.email],
            fail_silently=False,
        )
        return f"Payout notification sent for vendor: {payout.vendor.username}"
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)