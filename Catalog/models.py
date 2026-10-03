from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم القسم")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="الرابط المختصر (Slug)")
    # علاقة ذاتية للأقسام الفرعية والرئيسية
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name="القسم الرئيسي"
    )
    is_active = models.BooleanField(default=True, verbose_name="نشط؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "قسم"
        verbose_name_plural = "الأقسام"

    def __str__(self):
        return self.name


class Product(models.Model):
    # علاقة مع البائع (CustomUser)
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="البائع"
    )
    # علاقة مع القسم (Category)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        verbose_name="القسم"
    )
    title = models.CharField(max_length=255, verbose_name="عنوان المنتج")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="الرابط المختصر (Slug)")
    description = models.TextField(verbose_name="وصف المنتج")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    compare_at_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="السعر قبل الخصم"
    )
    is_active = models.BooleanField(default=True, verbose_name="منشور ومتاح؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "منتج"
        verbose_name_plural = "المنتجات"

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    # علاقة مع المنتج (Product)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="المنتج"
    )
    image = models.ImageField(upload_to='products/images/', verbose_name="صورة المنتج")
    is_feature = models.BooleanField(default=False, verbose_name="صورة رئيسية؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الرفع")

    class Meta:
        verbose_name = "صورة منتج"
        verbose_name_plural = "صور المنتجات"

    def __str__(self):
        return f"صورة لـ {self.product.title}"


class ProductAttribute(models.Model):
    # علاقة مع المنتج (Product)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='attributes',
        verbose_name="المنتج"
    )
    name = models.CharField(max_length=100, verbose_name="اسم الخاصية (مثال: اللون)")
    value = models.CharField(max_length=255, verbose_name="القيمة (مثال: أحمر)")

    class Meta:
        verbose_name = "خاصية منتج"
        verbose_name_plural = "خصائص المنتجات"

    def __str__(self):
        return f"{self.name}: {self.value} ({self.product.title})"