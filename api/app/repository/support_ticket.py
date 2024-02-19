from sqlalchemy.orm import Session, lazyload

import models.support_ticket as models
import schemas.support_ticket as schemas


def create(db: Session, ticket: schemas.SupportTicketCreate):
    db_session = models.SupportTicket(**ticket.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def create_event(db: Session, event: schemas.SupportTicketCreateEvent):
    db_session = models.SupportTicket(**event.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_support_ticket_by_id(db: Session, id: int):
    return db.query(models.SupportTicket).filter(models.SupportTicket.id == id).first()


def get_support_ticket_list_by_user(db: Session, user_id: int):
    return (
        db.query(models.SupportTicket)
        .filter(models.SupportTicket.open_by_id == user_id)
        .all()
    )


def get_event_list_by_ticket(db: Session, ticket_id: int):
    return (
        db.query(models.SuppportTicketEvent)
        .filter(models.SuppportTicketEvent.support_ticket == ticket_id)
        .all()
    )


def get_support_ticket_all(db: Session):
    return db.query(models.SupportTicket).all()


def accept_ticket(db: Session, ticket_id: int, user_id: int):
    ticket = (
        db.query(models.SupportTicket)
        .filter(models.SupportTicket.id == ticket_id)
        .first()
    )
    if ticket:
        ticket.assign_to_id = user_id
        ticket.status = "replied"
        db.commit()
        db.refresh(ticket)
    return ticket


def toggle_mark_resolve(db: Session, ticket_id: int):
    ticket = (
        db.query(models.SupportTicket)
        .filter(models.SupportTicket.id == ticket_id)
        .first()
    )
    if ticket:
        ticket.mark_resolved = not ticket.mark_resolved
        db.commit()
        db.refresh(ticket)
    return ticket


def toggle_push_notification(db: Session, ticket_id: int):
    ticket = (
        db.query(models.SupportTicket)
        .filter(models.SupportTicket.id == ticket_id)
        .first()
    )
    if ticket:
        ticket.push_notification = not ticket.push_notification
        db.commit()
        db.refresh(ticket)
    return ticket


def toggle_push_email(db: Session, ticket_id: int):
    ticket = (
        db.query(models.SupportTicket)
        .filter(models.SupportTicket.id == ticket_id)
        .first()
    )
    if ticket:
        ticket.push_email = not ticket.push_email
        db.commit()
        db.refresh(ticket)
    return ticket


def close(db: Session, ticket_id: int):
    ticket = (
        db.query(models.SupportTicket)
        .filter(models.SupportTicket.id == ticket_id)
        .first()
    )
    if ticket:
        ticket.status = "close"
        db.commit()
        db.refresh(ticket)
    return ticket


def reopen(db: Session, ticket_id: int):
    ticket = (
        db.query(models.SupportTicket)
        .filter(models.SupportTicket.id == ticket_id)
        .first()
    )
    if ticket:
        ticket.status = "replied"
        db.commit()
        db.refresh(ticket)
    return ticket
