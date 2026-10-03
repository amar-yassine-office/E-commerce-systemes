from django.utils import timezone
from .models import Invoice, PaymentTransaction, VendorPayout
from .tasks import (
    send_invoice_notification_task,
    verify_payment_transaction_task,
    send_vendor_payout_notification_task
)




class AccountantService:

    @staticmethod
    def create_invoice(customer, order_id, total_amount, tax_amount=0.00):
        """
        Creates an invoice and triggers the background email task.
        """
        invoice = Invoice.objects.create(
            customer=customer,
            order_id=order_id,
            total_amount=total_amount,
            tax_amount=tax_amount,
            status=Invoice.InvoiceStatus.PENDING
        )

        # Trigger Celery task asynchronously
        send_invoice_notification_task.delay(invoice.id)
        return invoice

    @staticmethod
    def record_payment_transaction(invoice, gateway, transaction_id, amount, status):
        """
        Records a payment transaction and triggers verification/processing task.
        """
        transaction = PaymentTransaction.objects.create(
            invoice=invoice,
            gateway=gateway,
            transaction_id=transaction_id,
            amount=amount,
            status=status
        )

        if status == PaymentTransaction.PaymentStatus.PENDING:
            # Trigger asynchronous verification task
            verify_payment_transaction_task.delay(transaction.id)

        return transaction

    @staticmethod
    def process_payout(payout_id, accountant_user):
        """
        Marks a vendor payout as paid and triggers the notification email task.
        """
        try:
            payout = VendorPayout.objects.get(id=payout_id)
            payout.status = VendorPayout.PayoutStatus.PAID
            payout.processed_by = accountant_user
            payout.paid_at = timezone.now()
            payout.save()

            # Trigger Celery notification task
            send_vendor_payout_notification_task.delay(payout.id)
            return payout
        except VendorPayout.DoesNotExist:
            return None









