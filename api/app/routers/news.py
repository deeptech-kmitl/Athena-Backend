from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from middleware.auth import get_auth_user, AuthDep
from database.engine import SessionLocal
from sqlalchemy import Column, Integer, String, Boolean

import schemas.news as schemas
import repository.news as repo

router = APIRouter(
    prefix="/news",
    tags=["News"],
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


@router.get("", response_model=list[schemas.News])
async def get_news(db: Session = Depends(get_db)):
    return repo.get_publish_news_list(db)


@router.get("/popup", response_model=list[schemas.News])
async def get_popup_news(db: Session = Depends(get_db)):
    return repo.get_popup_publish_news_list(db)


# admin
@router.get("/admin", response_model=list[schemas.News])
async def admin_get_news(db: Session = Depends(get_db)):
    return repo.get_news_list(db)


@router.put("/admin", response_model=schemas.News)
async def admin_create_news(
    news_create: schemas.NewsCreate,
    auth: AuthDep,
    db: Session = Depends(get_db),
):
    news_create.author_id = auth.user.id
    if news_create.status != "publish":
        news_create.status = "draft"
    news = repo.create(db, news_create)
    if news:
        return news
    raise HTTPException(404)


@router.get("/admin/{id}", response_model=schemas.News)  # list
async def admin_get_news_by_id(id: int, db: Session = Depends(get_db)):
    news = repo.get_news(db, id)
    if news:
        return news
    raise HTTPException(404)


@router.patch("/admin/{id}", response_model=schemas.News)
async def admin_update_news(
    id: int, news_save: schemas.NewsSave, db: Session = Depends(get_db)
):
    news = repo.get_news(db, id)
    if news:
        news_save.id = id
        return repo.save(db, news_save)
    raise HTTPException(404)


@router.post("/admin/{id}/publish", response_model=schemas.News)
async def admin_publish_news(id: int, db: Session = Depends(get_db)):
    news = repo.get_news(db, id)
    if news:
        return repo.publish(db, id)
    raise HTTPException(404)


@router.post("/admin/{id}/unpublish", response_model=schemas.News)
async def admin_unpublish_news(id: int, db: Session = Depends(get_db)):
    news = repo.get_news(db, id)
    if news:
        return repo.unpublish(db, id)
    raise HTTPException(404)


@router.get("/{id}", response_model=schemas.News)
async def get_news_by_id(id: int, db: Session = Depends(get_db)):
    news = repo.get_news(db, id)
    if news:
        if news != "publish":
            raise HTTPException(403, "No permission to read this news not publish")
        return news
    raise HTTPException(404)
