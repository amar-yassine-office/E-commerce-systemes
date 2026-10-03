from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Product


@shared_task(bind=True, max_retries=3)
def optimize_product_image_task(self, image_id):
    """
    Background task to process, resize, or optimize uploaded product images.
    """
    try:
        from .models import ProductImage
        product_image = ProductImage.objects.get(id=image_id)

        # Here you can add your image processing logic using Pillow (PIL)
        # e.g., resizing dimensions, compressing quality, converting to WebP format.

        return f"Image optimized successfully for Product Image ID: {image_id}"
    except Exception as exc:
        raise self.retry(exc=exc, countdown=30)


@shared_task(bind=True, max_retries=3)
def notify_vendor_product_status_task(self, product_id):
    """
    Background task to notify a vendor when their product is created or updated.
    """
    try:
        product = Product.objects.get(id=product_id)
        subject = f"Product Status Update: {product.title}"
        message = (
            f"Dear {product.vendor.username},\n\n"
            f"Your product '{product.title}' has been successfully registered/updated.\n"
            f"Current Status: {'Active & Published' if product.is_active else 'Inactive'}\n\n"
            f"Best regards,\nPlatform Team"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [product.vendor.email],
            fail_silently=False,
        )
        return f"Product notification sent for Vendor: {product.vendor.username}"
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)