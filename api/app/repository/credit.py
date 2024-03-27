from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session, lazyload

from models.sort import SortBy
import models.credit as models
import schemas.credit as schemas
import models.user as modelsUsr


def get_credit_trasaction_list(
    db: Session,
    filter: Optional[schemas.CreditTransactionFilter],
    limit: int = 10,
    page: int = 1,
):
    offset = (page - 1) * limit
    query = select(models.CreditTransaction).limit(limit).offset(offset)
    if filter is not None:
        query = filter.sort(query)
    result = db.execute(query)

    return result.scalars().all()


def transfer_credit(
    db: Session,
    detail: str,
    user_id: int,
    target_id: int,
    amount: int,
):
    user = (
        db.query(modelsUsr.User)
        .filter(modelsUsr.User.id == user_id, modelsUsr.User.credit >= amount)
        .first()
    )
    if user:
        user.credit = user.credit - amount
        db.commit()
        db.refresh(user)
    else:
        return
    target = db.query(modelsUsr.User).filter(modelsUsr.User.id == target_id).first()
    if target:
        target.credit = target.credit + amount
        db.commit()
        db.refresh(target)
    else:
        return
    transaction = models.CreditTransaction(
        detail=detail, amount=amount, user_id=user_id, target_id=target_id
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
