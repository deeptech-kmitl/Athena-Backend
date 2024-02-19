from pydantic import BaseModel
from . import user


class SupportTicketBase(BaseModel):
    pass


class SupportTicketCreate(SupportTicketBase):
    user_id: int
    title: str
    priority: str
    status: str
    push_notification: bool
    push_email: bool


class SupportTicketCreateEvent(SupportTicketBase):
    event_type: str
    message: str
    file: str
    reply: bool
    user_id: int
    support_ticket_id: int


class SupportTicket(SupportTicketBase):
    id: int
    title: str
    priority: int

    status: str
    push_notification: bool
    push_email: bool
    mark_resolved: bool

    assign_to_id: int
    assign_to: user.User

    created: str
    updated: str

    class Config:
        orm_mode = True


class SupportTicketEventBase(BaseModel):
    pass


class SupportTicketEvent(SupportTicketEventBase):
    event_type: str

    message: str
    file: str

    read: bool
    reply: bool

    created: str
    updated: str

    class Config:
        orm_mode = True


class SupportTicketEventAdmin(SupportTicketEventBase):
    user_id: int
    user: user.User

    class Config:
        orm_mode = True
