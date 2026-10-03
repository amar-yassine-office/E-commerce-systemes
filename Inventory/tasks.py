from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import StockItem


@shared_task(bind=True, max_retries=3)
def check_low_stock_task(self, stock_item_id):
    """
    Background task to check if a product's stock has fallen below the threshold
    and alert the platform managers or the product vendor.
    """
    try:
        stock_item = StockItem.objects.select_related('warehouse', 'product', 'product__vendor').get(id=stock_item_id)

        # Check if quantity is less than or equal to the low stock threshold
        if stock_item.quantity <= stock_item.low_stock_threshold:
            vendor_email = stock_item.product.vendor.email
            subject = f"Low Stock Alert: {stock_item.product.title}"
            message = (
                f"Attention,\n\n"
                f"The product '{stock_item.product.title}' in warehouse '{stock_item.warehouse.name}' "
                f"is running low on stock.\n"
                f"Current Available Quantity: {stock_item.quantity}\n"
                f"Low Stock Threshold: {stock_item.low_stock_threshold}\n\n"
                f"Please restock soon to avoid running out of inventory."
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [vendor_email],
                fail_silently=False,
            )
            return f"Low stock alert email sent for Product: {stock_item.product.title}"

        return f"Stock level is safe for Product ID: {stock_item.product.id}"
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)