from typing import List, Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel
import models.credit as models


class CreditTransactionBase(BaseModel):
    amount: int


class CreditTransactionCreate(CreditTransactionBase):
    amount: int
    email: str


class CreditTransactionSave(CreditTransactionBase):
    pass


class CreditTransaction(CreditTransactionBase):
    id: int
    detail: str

    class Config:
        orm_mode = True


class CreditTransactionAdmin(CreditTransactionBase):
    id: int
    detail: str

    class Config:
        orm_mode = True


class CreditTransactionFilter(Filter):
    order_by: List[str] = ["amount"]

    class Constants(Filter.Constants):
        model = models.CreditTransaction
