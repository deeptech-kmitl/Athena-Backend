from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
# from fastapi.staticfiles import StaticFiles

router = APIRouter(
    prefix="/ticket", 
    tags=["Ticket"], 
    responses={404: {"message": "Not found"}}
)

tickets_db = []

class Ticket(BaseModel):
    subject: str
    description: str
    replies: List[str] = []
    statusTicket: str
    
# router.mount("/static", StaticFiles(directory="static"), name="static")

@router.post("/createTicket")
async def create_ticket(ticket: Ticket):
    tickets_db.append(ticket)
    return ticket

@router.get("/allTickets")
async def read_tickets(status: Optional[str] = None) -> List[Ticket]:
    if status:
        return [t for t in tickets_db if t.status == status]
    return tickets_db

@router.get("/ticket")
async def read_ticket(ticket_id: int) -> Ticket:
    return tickets_db[ticket_id]

@router.post("/tickets/{ticket_id}/reply")
async def reply_to_ticket(ticket_id: int, reply: str):
    tickets_db[ticket_id].replies.append(reply)
    return tickets_db[ticket_id]