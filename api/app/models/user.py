from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.engine import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    credit = Column(Float, default=0)
    # role_id = Column(Integer, ForeignKey("roles.id"))

    # role = relationship("Role", back_populates="users")

    sessions = relationship("Session", back_populates="user", lazy=True)
    news = relationship("News", back_populates="author", lazy=True)
    support_ticket_events = relationship(
        "SuppportTicketEvent", back_populates="user", lazy=True
    )
    instances = relationship("Instance", back_populates="owner", lazy=True)

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_revoke = Column(Boolean, default=False)
    user_agent = Column(String)

    user = relationship("User", back_populates="sessions", lazy=False)

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
