from ninja import Router
from typing import List
from ninja_jwt.authentication import JWTAuth
from .schemas import (
    SupportTicketCreateSchema, SupportTicketOutSchema, SupportTicketUpdateSchema,
    ReturnRequestCreateSchema, ReturnRequestOutSchema, ReturnRequestUpdateSchema
)
from .services import AgentService

router = Router(tags=["Customer Support & Agent Operations"])

# --- Support Tickets Endpoints ---
@router.post("/tickets/", response=SupportTicketOutSchema, auth=JWTAuth())
def create_ticket(request, payload: SupportTicketCreateSchema):
    return AgentService.create_ticket(request.auth, payload.dict())

@router.get("/tickets/", response=List[SupportTicketOutSchema], auth=JWTAuth())
def list_tickets(request):
    return AgentService.get_all_tickets()

@router.patch("/tickets/{ticket_id}", response=SupportTicketOutSchema, auth=JWTAuth())
def update_ticket(request, ticket_id: int, payload: SupportTicketUpdateSchema):
    return AgentService.update_ticket(ticket_id, payload.dict())

# --- Return Requests Endpoints ---
@router.post("/returns/", response=ReturnRequestOutSchema, auth=JWTAuth())
def create_return_request(request, payload: ReturnRequestCreateSchema):
    return AgentService.create_return_request(request.auth, payload.dict())

@router.get("/returns/", response=List[ReturnRequestOutSchema], auth=JWTAuth())
def list_return_requests(request):
    return AgentService.get_all_return_requests()

@router.patch("/returns/{request_id}/process", response=ReturnRequestOutSchema, auth=JWTAuth())
def process_return(request, request_id: int, payload: ReturnRequestUpdateSchema):
    return AgentService.process_return_request(request_id, payload.status, request.auth)