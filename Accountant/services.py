from django.shortcuts import get_object_or_404
from .models import Invoice, PaymentTransaction, VendorPayout
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountantService:

    @staticmethod
    def create_invoice(data: dict) -> Invoice:
        customer = get_object_or_404(User, id=data.pop('customer_id'))
        invoice = Invoice.objects.create(customer=customer, **data)
        return invoice

    @staticmethod
    def get_all_invoices() -> list[Invoice]:
        return Invoice.objects.all().order_by('-issued_at')

    @staticmethod
    def get_invoice_by_id(invoice_id: int) -> Invoice:
        return get_object_or_404(Invoice, id=invoice_id)

    @staticmethod
    def create_transaction(data: dict) -> PaymentTransaction:
        invoice = get_object_or_404(Invoice, id=data.pop('invoice_id'))
        transaction = PaymentTransaction.objects.create(invoice=invoice, **data)
        return transaction

    @staticmethod
    def get_invoice_transactions(invoice_id: int) -> list[PaymentTransaction]:
        return PaymentTransaction.objects.filter(invoice_id=invoice_id)

    @staticmethod
    def create_payout(data: dict) -> VendorPayout:
        vendor = get_object_or_404(User, id=data.pop('vendor_id'))
        payout = VendorPayout.objects.create(vendor=vendor, **data)
        return payout

    @staticmethod
    def process_payout(payout_id: int, accountant_user) -> VendorPayout:
        payout = get_object_or_404(VendorPayout, id=payout_id)
        payout.status = VendorPayout.PayoutStatus.APPROVED
        payout.processed_by = accountant_user
        payout.save()
        return payout