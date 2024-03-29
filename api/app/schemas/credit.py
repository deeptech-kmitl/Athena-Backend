from typing import List, Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel
import models.credit as models


class CreditTransactionBase(BaseModel):
    amount: float


class CreditTransactionCreate(CreditTransactionBase):
    amount: float
    email: str


class CreditTransactionSave(CreditTransactionBase):
    pass


class CreditTransaction(CreditTransactionBase):
    id: int
    detail: str

    class Config:
        from_attributes = True


class CreditTransactionAdmin(CreditTransactionBase):
    id: int
    detail: str

    class Config:
        from_attributes = True


class CreditTransactionFilter(Filter):
    order_by: List[str] = ["amount"]

    class Constants(Filter.Constants):
        model = models.CreditTransaction
