from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
# from fastapi.staticfiles import StaticFiles

router = APIRouter(
    prefix="/ticket", 
    tags=["Ticket"], 
    responses={404: {"message": "Not found"}}
)

tickets_db = [
    {
  "subject": "test0",
  "description": "testDB",
  "statusTicket": "Accept"
},
    {
  "subject": "test1",
  "description": "testDB",
  "statusTicket": "Complete"
}
]
replies_db = [
    {
    "ticketID": 1,
    "reply": "…"
  },
    {
    "ticketID": 0,
    "reply": "test"
  }
]

class Ticket(BaseModel):
    subject: str
    description: str
    # replies: List[str] = []
    statusTicket: str
    
class Reply(BaseModel):
    ticketID: int
    reply: str
    
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

@router.get("/allReplies")
async def read_replies(status: Optional[str] = None) -> List[Reply]:
    if status:
        return [t for t in replies_db if t.status == status]
    return replies_db

@router.post("/tickets/{ticket_id}/reply")
async def reply_to_ticket(ticket_id: int, reply: Reply):
    replies_db.append(reply)
    return reply

@router.put("/tickets/admin/{ticket_id}/reply")
async def reply_to_ticket_admin(ticket_id: int, reply: Reply):
    ticket = Ticket(**tickets_db[ticket_id])
    if ticket.statusTicket == "Accept":
        replies_db.append(reply)
        return reply
    elif ticket.statusTicket == "Reject":
        return {"message": "Ticket in 'Reject' status"}
    elif ticket.statusTicket == "Complete":
        return {"message": "Ticket in 'Completed' status"}
    else:
        return {"message": "Ticket not in 'Accept' status"}
