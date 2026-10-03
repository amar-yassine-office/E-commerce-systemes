from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class VendorProfile(models.Model):
    class VerificationStatus(models.TextChoices):
        PENDING = 'pending', 'Pending Verification'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        SUSPENDED = 'suspended', 'Suspended'

    # Relationship with CustomUser (Each vendor is a user with a vendor role)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vendor_profile',
        verbose_name="User Account"
    )
    store_name = models.CharField(max_length=255, unique=True, verbose_name="Store Name")
    store_slug = models.SlugField(max_length=255, unique=True, verbose_name="Store Slug")
    store_description = models.TextField(blank=True, null=True, verbose_name="Store Description")
    logo = models.ImageField(upload_to='vendors/logos/', blank=True, null=True, verbose_name="Store Logo")
    banner = models.ImageField(upload_to='vendors/banners/', blank=True, null=True, verbose_name="Store Banner")

    # Verification & Financials
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        verbose_name="Verification Status"
    )
    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.00,
        verbose_name="Commission Rate (%)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Registration Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        verbose_name = "Vendor Profile"
        verbose_name_plural = "Vendor Profiles"

    def __str__(self):
        return f"{self.store_name} ({self.user.username})"


class VendorBankDetail(models.Model):
    # Relationship with VendorProfile
    vendor = models.OneToOneField(
        VendorProfile,
        on_delete=models.CASCADE,
        related_name='bank_detail',
        verbose_name="Vendor"
    )
    bank_name = models.CharField(max_length=100, verbose_name="Bank Name")
    account_holder_name = models.CharField(max_length=255, verbose_name="Account Holder Name")
    account_number = models.CharField(max_length=100, verbose_name="Account Number / IBAN")
    swift_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="SWIFT / BIC Code")
    is_verified = models.BooleanField(default=False, verbose_name="Is Bank Account Verified?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Vendor Bank Detail"
        verbose_name_plural = "Vendor Bank Details"

    def __str__(self):
        return f"Bank Details for {self.vendor.store_name} - {self.bank_name}"