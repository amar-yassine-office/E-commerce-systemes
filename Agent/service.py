from .models import SupportTicket, ReturnRequest
from .tasks import send_ticket_notification_task, send_return_request_status_task

class AgentService:

    @staticmethod
    def create_support_ticket(customer, subject, description, priority=SupportTicket.Priority.MEDIUM):
        """
        Creates a support ticket and triggers a background email notification to the customer.
        """
        ticket = SupportTicket.objects.create(
            customer=customer,
            subject=subject,
            description=description,
            priority=priority,
            status=SupportTicket.TicketStatus.OPEN
        )

        # Trigger Celery background task
        send_ticket_notification_task.delay(ticket.id)
        return ticket

    @staticmethod
    def update_return_request_status(return_request_id, new_status, agent_user):
        """
        Updates a return request status, assigns the processing agent, and triggers a notification task.
        """
        try:
            return_req = ReturnRequest.objects.get(id=return_request_id)
            return_req.status = new_status
            return_req.processed_by = agent_user
            return_req.save()

            # Trigger Celery background task
            send_return_request_status_task.delay(return_req.id)
            return return_req
        except ReturnRequest.DoesNotExist:
            return None

        from cache import RedisCacheManager
        from .models import SupportTicket, ReturnRequest
        from .tasks import send_ticket_notification_task, send_return_request_status_task
        from django.db.models import Count

        class AgentService:

            @staticmethod
            def get_ticket_statistics():
                stats = RedisCacheManager.get_agent_ticket_stats()

                if stats is not None:
                    return stats

                stats = list(SupportTicket.objects.values('status').annotate(total=Count('id')))

                RedisCacheManager.set_agent_ticket_stats(stats, timeout=60 * 5)
                return stats

            @staticmethod
            def create_support_ticket(customer, subject, description, priority=SupportTicket.Priority.MEDIUM):
                ticket = SupportTicket.objects.create(
                    customer=customer,
                    subject=subject,
                    description=description,
                    priority=priority,
                    status=SupportTicket.TicketStatus.OPEN
                )

                RedisCacheManager.clear_agent_ticket_stats()
                send_ticket_notification_task.delay(ticket.id)
                return ticket

            @staticmethod
            def update_return_request_status(return_request_id, new_status, agent_user):
                try:
                    return_req = ReturnRequest.objects.get(id=return_request_id)
                    return_req.status = new_status
                    return_req.processed_by = agent_user
                    return_req.save()

                    send_return_request_status_task.delay(return_req.id)
                    return return_req
                except ReturnRequest.DoesNotExist:
                    return None