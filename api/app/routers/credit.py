from typing import Optional
from fastapi import FastAPI, File, Query, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils.sort import parse_sort
from middleware.auth import get_auth_user, AuthDep
from database.engine import SessionLocal
from sqlalchemy import Column, Integer, String, Boolean

import schemas.credit as schemas
import repository.credit as repo
import repository.user as usrRepo
from fastapi_filter.contrib.sqlalchemy import Filter

router = APIRouter(
    prefix="/credit",
    tags=["Credit"],
    responses={404: {"message": "Not found"}},
    dependencies=[Depends(get_auth_user)],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("")
async def get_credit(auth: AuthDep):
    return {"message": "ok", "credit": auth.user.credit}


@router.get("/transaction", response_model=list[schemas.CreditTransaction])
async def get_credit_transaction(
    user_filter: schemas.CreditTransactionFilter = FilterDepends(
        schemas.CreditTransactionFilter,
    ),
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=50),
    page: int = Query(1, ge=1),
):
    return repo.get_credit_trasaction_list(db, user_filter, limit, page)


@router.post("/transfer", response_model=schemas.CreditTransaction)
async def get_credit_transaction(
    auth: AuthDep,
    create: schemas.CreditTransactionCreate,
    db: Session = Depends(get_db),
):
    if auth.user.credit < create.amount:
        raise HTTPException(400, "user credit not enought")
    targetUser = usrRepo.get_user_by_email(db, create.email)
    if targetUser is None:
        raise HTTPException(400, "email not found")
    transaction = repo.transfer_credit(
        db, "Transfer credit", auth.user.id, targetUser.id, create.amount
    )
    if transaction is None:
        raise HTTPException(500, "something went wrong")
    return transaction
