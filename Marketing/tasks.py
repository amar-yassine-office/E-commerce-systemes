from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import NewsletterSubscriber

@shared_task(bind=True, max_retries=3)
def send_newsletter_welcome_task(self, subscriber_id):
    """
    Background task to send a welcome email to a new newsletter subscriber.
    """
    try:
        subscriber = NewsletterSubscriber.objects.get(id=subscriber_id)
        subject = "Welcome to Our Newsletter & Special Offers!"
        message = (
            f"Hello,\n\n"
            f"Thank you for subscribing to our newsletter with email: {subscriber.email}.\n"
            f"Stay tuned for our latest discounts, promotions, and exclusive updates!\n\n"
            f"Best regards,\nPlatform Team"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [subscriber.email],
            fail_silently=False,
        )
        return f"Newsletter welcome email sent to: {subscriber.email}"
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)