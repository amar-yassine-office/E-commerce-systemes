from django.db import models

# Create your models here.
from django.db import models


class CryptoTransaction(models.Model):
  # ربط المعاملة بالطلب الأساسي في متجرك (سواء كان Order أو Invoice)
  # order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='crypto_transactions')

  # بيانات المعاملة القادمة من NOWPayments
  payment_id = models.CharField(
      max_length=100, unique=True, help_text='معرف الفاتورة في NOWPayments'
  )
  payment_status = models.CharField(
      max_length=50,
      default='waiting',
      help_text='حالة الدفع: waiting, confirming, confirmed, failed, etc.',
  )
  pay_address = models.CharField(
      max_length=255, help_text='عنوان المحفظة التي سيحول عليها العميل'
  )
  price_amount = models.DecimalField(
      max_digits=12, decimal_places=2, help_text='المبلغ بالقيمة المطلوبة (USD مثلاً)'
  )
  price_currency = models.CharField(
      max_length=10, default='usd', help_text='عملة التسعير الأساسية'
  )
  pay_currency = models.CharField(
      max_length=10, help_text='العملة الرقمية المختارة للدفع مثل btc, usdt'
  )
  pay_amount = models.DecimalField(
      max_digits=18, decimal_places=8, help_text='المبلغ المطلوب بالعملة الرقمية'
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return (
        f'Crypto Payment {self.payment_id} - Status: {self.payment_status}'
    )