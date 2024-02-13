from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean

DATABASE_URL = ""
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    popup = Column(Boolean)

# class News(BaseModel):
#     title: str
#     content: str
#     popup: bool

# news_data = [
#     {'id': 1, 'title': 'News 1', 'content': 'This news1.', 'popup': False},
#     {'id': 2, 'title': 'News 2', 'content': 'This news2.', 'popup': True},
# ]

@router.get("/news/", response_model=List[News])
async def read_news(db: Session = Depends(get_db)):
    return db.query(News).all()

@router.get("/newspopup/", response_model=News )
async def read_newspopup(db: Session = Depends(get_db)):
    newspopup = next((n for n in news_data if n['popup']), None)
    if newspopup:
        return newspopup
    raise HTTPException(status_code=404)

#admin
@router.post("/news/admin/", response_model=News) #create
async def create_news(news: News, db: Session = Depends(get_db)):
    news_id = len(news_data) + 1
    news_item = {'id': news_id, 'title': news.title, 'content': news.content}
    news_data.append(news_item)
    return news_item

@router.get("/news/admin/{news_id}", response_model=News) #list
async def read_news_item(news_id: int):
    news_item = next((n for n in news_data if n['id'] == news_id), None)
    if news_item:
        return news_item
    raise HTTPException(status_code=404)

@router.put("/news/admin/{news_id}", response_model=News) #update news
async def update_news(news_id: int, news: News):
    for n in news_data:
        if n['id'] == news_id:
            n['title'] = news.title
            n['content'] = news.content
            return n
    raise HTTPException(status_code=404)


@router.delete("/news/admin/{news_id}", response_model=News) #delete
async def delete_news(news_id: int, db: Session = Depends(get_db)):
    dbnews = db.query(News).filter(News.id == news_id).first()
    if dbnews:
        db.delete(dbnews)
        db.commit()
        return dbnews

@router.post("/news/upnews/admin/{news_id}", response_model=News) #upload img tham mai pen
async def upload_image(news_id: int, file: UploadFile = File(...)):
    upnews = await file.read()
    return  upnews #name file or link

