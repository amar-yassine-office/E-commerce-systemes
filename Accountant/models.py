from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Invoice(models.Model):
    class InvoiceStatus(models.TextChoices):
        PENDING = 'pending', 'قيد الانتظار'
        PAID = 'paid', 'مدفوعة'
        CANCELLED = 'cancelled', 'ملغاة'
        REFUNDED = 'refunded', 'مسترجعة'

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='invoices',
        verbose_name="العميل"
    )
    order_id = models.IntegerField(verbose_name="رقم الطلب المرتبط")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ الإجمالي")
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="قيمة الضريبة")
    status = models.CharField(
        max_length=20,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.PENDING,
        verbose_name="حالة الفاتورة"
    )
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإصدار")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    def __str__(self):
        return f"فاتورة #{self.id} - طلب #{self.order_id}"


class PaymentTransaction(models.Model):
    class PaymentGateway(models.TextChoices):
        STRIPE = 'stripe', 'Stripe'
        PAYPAL = 'paypal', 'PayPal'
        CASH_ON_DELIVERY = 'cod', 'الدفع عند الاستلام'

    class PaymentStatus(models.TextChoices):
        SUCCESS = 'success', 'ناجحة'
        FAILED = 'failed', 'فاشلة'
        PENDING = 'pending', 'معلقة'

    # علاقة ForeignKey مع جدول الفواتير (Invoice -> PaymentTransaction)
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name="الفاتورة المرتبطة"
    )
    gateway = models.CharField(
        max_length=50,
        choices=PaymentGateway.choices,
        verbose_name="بوابة الدفع"
    )
    transaction_id = models.CharField(max_length=255, unique=True, verbose_name="معرف المعاملة (Gateway Tx ID)")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ المدفوع")
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name="حالة الدفع"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ المعاملة")

    def __str__(self):
        return f"معاملة #{self.transaction_id} - {self.get_status_display()}"


class VendorPayout(models.Model):
    class PayoutStatus(models.TextChoices):
        PENDING = 'pending', 'قيد المعالجة'
        APPROVED = 'approved', 'تمت الموافقة'
        PAID = 'paid', 'تم التحويل'

    # علاقة مع البائع (CustomUser)
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payouts',
        verbose_name="البائع"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ المستحقات")
    commission_deducted = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="عمولة المنصة المخصومة")
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="الصافي المحول للبائع")
    status = models.CharField(
        max_length=20,
        choices=PayoutStatus.choices,
        default=PayoutStatus.PENDING,
        verbose_name="حالة التحويل"
    )
    # علاقة مع المحاسب المسؤول (CustomUser)
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_payouts',
        verbose_name="المحاسب المسؤول"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="تاريخ التحويل الفعلي")

    def __str__(self):
        return f"مستحقات البائع #{self.vendor.username} - {self.net_amount}"