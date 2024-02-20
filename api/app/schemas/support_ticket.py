from pydantic import BaseModel
from . import user


class SupportTicketBase(BaseModel):
    pass


class SupportTicketCreate(SupportTicketBase):
    open_by_id: int
    title: str
    message: str
    priority: int
    status: str
    push_notification: bool
    push_email: bool


class SupportTicketCreateEvent(SupportTicketBase):
    event_type: str = "message"
    message: str = ""
    file: str = ""
    user_id: int
    support_ticket_id: int
    reply: bool = False


class SupportTicket(SupportTicketBase):
    id: int
    title: str
    priority: int

    status: str
    push_notification: bool
    push_email: bool
    mark_resolved: bool

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

    class Config:
        orm_mode = True


class SupportTicketEventAdmin(SupportTicketEventBase):
    user_id: int
    user: user.User

    class Config:
        orm_mode = True
