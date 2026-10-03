from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class SupportTicket(models.Model):
    class TicketStatus(models.TextChoices):
        OPEN = 'open', 'مفتوحة'
        IN_PROGRESS = 'in_progress', 'قيد المعالجة'
        RESOLVED = 'resolved', 'تم الحل'
        CLOSED = 'closed', 'مغلقة'

    class Priority(models.TextChoices):
        LOW = 'low', 'منخفضة'
        MEDIUM = 'medium', 'متوسطة'
        HIGH = 'high', 'عالية'
        URGENT = 'urgent', 'عاجلة'

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='support_tickets',
        verbose_name="العميل"
    )
    assigned_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets',
        verbose_name="الموظف المسؤول (Agent)"
    )
    subject = models.CharField(max_length=255, verbose_name="عنوان المشكلة")
    description = models.TextField(verbose_name="تفاصيل المشكلة")
    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.OPEN,
        verbose_name="حالة التذكرة"
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name="الأولوية"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    def __str__(self):
        return f"تذكرة #{self.id} - {self.subject}"


class ReturnRequest(models.Model):
    class ReturnStatus(models.TextChoices):
        PENDING = 'pending', 'قيد المراجعة'
        APPROVED = 'approved', 'تمت الموافقة'
        REJECTED = 'rejected', 'مرفوض'
        COMPLETED = 'completed', 'مكتمل'

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='return_requests',
        verbose_name="العميل"
    )
    order_id = models.IntegerField(verbose_name="رقم الطلب المرتبط")
    reason = models.TextField(verbose_name="سبب الإرجاع")
    status = models.CharField(
        max_length=20,
        choices=ReturnStatus.choices,
        default=ReturnStatus.PENDING,
        verbose_name="حالة الإرجاع"
    )
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_returns',
        verbose_name="الموظف المعالج"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")

    def __str__(self):
        return f"طلب إرجاع #{self.id} للطلب رقم #{self.order_id}"
