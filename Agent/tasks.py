from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import SupportTicket, ReturnRequest

@shared_task(bind=True, max_retries=3)
def send_ticket_notification_task(self, ticket_id):
    """
    Background task to notify a customer when a support ticket is created or updated.
    """
    try:
        ticket = SupportTicket.objects.get(id=ticket_id)
        subject = f"Support Ticket #{ticket.id} - {ticket.subject}"
        message = (
            f"Hello {ticket.customer.username},\n\n"
            f"Your support ticket has been registered successfully.\n"
            f"Current Status: {ticket.get_status_display()}\n"
            f"Priority: {ticket.get_priority_display()}\n\n"
            f"Our support team will get back to you soon."
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [ticket.customer.email],
            fail_silently=False,
        )
        return f"Support ticket email sent for Ticket ID: {ticket_id}"
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_return_request_status_task(self, return_request_id):
    """
    Background task to notify a customer about the status update of their return request.
    """
    try:
        return_req = ReturnRequest.objects.get(id=return_request_id)
        subject = f"Return Request Update - Order #{return_req.order_id}"
        message = (
            f"Dear {return_req.customer.username},\n\n"
            f"The status of your return request for order #{return_req.order_id} has been updated.\n"
            f"Current Status: {return_req.get_status_display()}\n\n"
            f"Thank you for your patience."
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [return_req.customer.email],
            fail_silently=False,
        )
        return f"Return status email sent for Request ID: {return_request_id}"
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)