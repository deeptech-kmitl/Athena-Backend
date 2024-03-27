from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.engine import Base


class CreditTransaction(Base):
    __tablename__ = "credit_transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, primary_key=True, index=True)
    detail = Column(String, primary_key=True, index=True)

    user_id = Column(Integer, index=True)
    user = relationship("User", back_populates="transactions")

    target_id = Column(Integer, index=True)
    target = relationship("User", back_populates="transactions_target")

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
