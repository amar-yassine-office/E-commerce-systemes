from django.shortcuts import get_object_or_404
from .models import SupportTicket, ReturnRequest
from django.contrib.auth import get_user_model

User = get_user_model()


class AgentService:

    # --- Support Tickets Services ---
    @staticmethod
    def create_ticket(customer, data: dict) -> SupportTicket:
        return SupportTicket.objects.create(customer=customer, **data)

    @staticmethod
    def get_all_tickets() -> list[SupportTicket]:
        return SupportTicket.objects.all().order_by('-created_at')

    @staticmethod
    def update_ticket(ticket_id: int, data: dict) -> SupportTicket:
        ticket = get_object_or_404(SupportTicket, id=ticket_id)
        for attr, value in data.items():
            if value is not None:
                if attr == 'assigned_agent_id' and value:
                    ticket.assigned_agent = get_object_or_404(User, id=value)
                else:
                    setattr(ticket, attr, value)
        ticket.save()
        return ticket

    # --- Return Requests Services ---
    @staticmethod
    def create_return_request(customer, data: dict) -> ReturnRequest:
        return ReturnRequest.objects.create(customer=customer, **data)

    @staticmethod
    def get_all_return_requests() -> list[ReturnRequest]:
        return ReturnRequest.objects.all().order_by('-created_at')

    @staticmethod
    def process_return_request(request_id: int, status: str, agent_user) -> ReturnRequest:
        return_req = get_object_or_404(ReturnRequest, id=request_id)
        return_req.status = status
        return_req.processed_by = agent_user
        return_req.save()
        return return_req