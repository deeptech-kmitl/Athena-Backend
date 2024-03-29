from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.engine import Base


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, index=True)
    priority = Column(Integer, default=0)

    status = Column(String, default="open")
    push_notification = Column(Boolean, default=False)
    push_email = Column(Boolean, default=False)
    mark_resolved = Column(Boolean, default=False)

    open_by_id = Column(
        Integer,
        ForeignKey(
            "users.id",
        ),
    )
    open_by = relationship(
        "User",
        foreign_keys=[open_by_id],
    )

    assign_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assign_to = relationship("User", foreign_keys=[assign_to_id])

    events = relationship(
        "SuppportTicketEvent", back_populates="support_ticket", lazy=True
    )

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class SuppportTicketEvent(Base):
    __tablename__ = "support_ticket_events"

    id = Column(Integer, primary_key=True, index=True)

    event_type = Column(String, default="message")

    message = Column(String, default="")
    file = Column(String, default="")

    read = Column(Boolean, default=False)
    reply = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="support_ticket_events")

    support_ticket_id = Column(Integer, ForeignKey("support_tickets.id"))
    support_ticket = relationship("SupportTicket", back_populates="events")

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
