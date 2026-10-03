from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import CryptoTransaction


@admin.register(CryptoTransaction)
class CryptoTransactionAdmin(admin.ModelAdmin):
  # الأعمدة التي ستظهر في جدول المعاملات
  list_display = (
      'payment_id',
      'pay_currency',
      'price_amount',
      'payment_status',
      'created_at',
  )

  # الفلاتر الجانبية لتسهيل البحث والتصفية
  list_filter = ('payment_status', 'pay_currency', 'created_at')

  # حقول البحث في لوحة التحكم
  search_fields = ('payment_id', 'pay_address')

  # جعل بعض الحقول للقراءة فقط حمايةً للبيانات المالية
  readonly_fields = (
      'payment_id',
      'pay_address',
      'pay_amount',
      'created_at',
      'updated_at',
  )