from pydantic import BaseModel
from . import user


class CreditTransactionBase(BaseModel):
    amount: int


class CreditTransactionCreate(CreditTransactionBase):
    detail: str
    user_id: int
    target_id: int


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
