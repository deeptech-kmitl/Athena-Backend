from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from middleware.auth import get_auth_user, AuthDep
from database.engine import SessionLocal
from sqlalchemy.orm import Session

import schemas.support_ticket as schemas
import repository.support_ticket as repo

# from fastapi.staticfiles import StaticFiles

router = APIRouter(
    prefix="/support-ticket",
    tags=["Support Ticket"],
    responses={404: {"message": "Not found"}},
    dependencies=[Depends(get_auth_user)],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.put("", response_model=schemas.SupportTicket)
async def create(
    create: schemas.SupportTicketCreate,
    auth: AuthDep,
    db: Session = Depends(get_db),
):
    create.open_by_id = auth.user.id
    create.status = "open"
    ticket = repo.create(db, create)
    repo.create_event(
        db,
        schemas.SupportTicketCreateEvent(
            event_type="message",
            message=create.message,
            support_ticket_id=ticket.id,
            user_id=auth.user.id,
        ),
    )
    if ticket:
        return ticket
    raise HTTPException(404)


@router.get("", response_model=list[schemas.SupportTicket])
async def get_ticket_list(
    auth: AuthDep,
    db: Session = Depends(get_db),
):
    return repo.get_support_ticket_list_by_user(db, auth.user.id)


@router.get("/{id}", response_model=schemas.SupportTicket)
async def get_ticket_by_id(id: int, db: Session = Depends(get_db)):
    ticket = repo.get_support_ticket_by_id(db, id)
    if ticket:
        return ticket
    raise HTTPException(404)


@router.get("/{id}/event", response_model=list[schemas.SupportTicketEvent])
async def get_ticket_event_by_id(id: int, db: Session = Depends(get_db)):
    events = repo.get_event_list_by_ticket(db, id)
    return events


@router.post("/{id}/reply", response_model=schemas.SupportTicketEvent)
async def reply_to_ticket(
    id: int,
    create: schemas.SupportTicketCreateEvent,
    auth: AuthDep,
    db: Session = Depends(get_db),
):
    ticket = repo.get_support_ticket_by_id(db, id)
    if ticket:
        create.support_ticket_id = id
        event = repo.create_event(
            db,
            create,
        )
        return event
    raise HTTPException(404)


@router.get("/admin", response_model=list[schemas.SupportTicket])
async def admin_get_ticket_list(
    auth: AuthDep,
    db: Session = Depends(get_db),
):
    return repo.get_support_ticket_all(db)


@router.get("admin/{id}", response_model=schemas.SupportTicket)
async def admin_get_ticket_by_id(id: int, db: Session = Depends(get_db)):
    ticket = repo.get_support_ticket_by_id(db, id)
    if ticket:
        return ticket
    raise HTTPException(404)


@router.get("admin/{id}/event", response_model=list[schemas.SupportTicketEvent])
async def admin_get_ticket_event_by_id(id: int, db: Session = Depends(get_db)):
    events = repo.get_event_list_by_ticket(db, id)
    return events


@router.post("admin/{id}/accept", response_model=schemas.SupportTicket)
async def admin_toggle_accept(
    id: int,
    auth: AuthDep,
    db: Session = Depends(get_db),
):
    ticket = repo.get_support_ticket_by_id(db, id)
    if ticket:
        ticket = repo.accept_ticket(db, ticket.id, auth.user.id)
        return ticket
    raise HTTPException(404)


@router.post("admin/{id}/mark-resolved", response_model=schemas.SupportTicket)
async def admin_toggle_mark_resolved(
    id: int,
    auth: AuthDep,
    db: Session = Depends(get_db),
):
    ticket = repo.get_support_ticket_by_id(db, id)
    if ticket:
        event = repo.toggle_mark_resolve(db, ticket.id, auth.user.id)
        return event
    raise HTTPException(404)


@router.post("admin/{id}/close", response_model=schemas.SupportTicket)
async def admin_close_ticket(
    id: int,
    auth: AuthDep,
    db: Session = Depends(get_db),
):
    ticket = repo.get_support_ticket_by_id(db, id)
    if ticket:
        event = repo.close(db, ticket.id, auth.user.id)
        return event
    raise HTTPException(404)


@router.post("admin/{id}/reopen", response_model=schemas.SupportTicket)
async def admin_reopen_ticket(
    id: int,
    auth: AuthDep,
    db: Session = Depends(get_db),
):
    ticket = repo.get_support_ticket_by_id(db, id)
    if ticket:
        event = repo.reopen(db, ticket.id, auth.user.id)
        return event
    raise HTTPException(404)


@router.post("admin/{id}/reply", response_model=schemas.SupportTicketEvent)
async def admin_reply_to_ticket(
    id: int,
    create: schemas.SupportTicketCreateEvent,
    auth: AuthDep,
    db: Session = Depends(get_db),
):
    ticket = repo.get_support_ticket_by_id(db, id)
    if ticket:
        create.support_ticket_id = id
        create.reply = True
        event = repo.create_event(
            db,
            create,
        )
        return event
    raise HTTPException(404)
