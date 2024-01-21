from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class News(BaseModel):
    title: str
    content: str
    popup: bool

news_data = [
    {'id': 1, 'title': 'News 1', 'content': 'This news1.', 'popup': False},
    {'id': 2, 'title': 'News 2', 'content': 'This news2.', 'popup': True},
]

@router.get("/news/", response_model=List[News])
def read_news():
    return news_data

@router.get("/newspopup/", response_model=News )
def read_newspopup():
    newspopup = next((n for n in news_data if n['popup']), None)
    if newspopup:
        return newspopup
    raise HTTPException(status_code=404)

@router.post("/news/admin/", response_model=News)
def create_news(news: News):
    news_id = len(news_data) + 1
    news_item = {'id': news_id, 'title': news.title, 'content': news.content}
    news_data.append(news_item)
    return news_item

@router.get("/news/admin/{news_id}", response_model=News)
def read_news_item(news_id: int):
    news_item = next((n for n in news_data if n['id'] == news_id), None)
    if news_item:
        return news_item
    raise HTTPException(status_code=404)

@router.put("/news/{news_id}", response_model=News) #update news
def update_news(news_id: int, news: News):
    for n in news_data:
        if n['id'] == news_id:
            n['title'] = news.title
            n['content'] = news.content
            return n
    raise HTTPException(status_code=404)


@router.delete("/news/{news_id}", response_model=News)
def delete_news(news_id: int):
    news = news_data.pop(news_id - 1)
    return news

@router.post("/news/upnews/{news_id}", response_model=News)
async def upload_image(news_id: int, file: UploadFile = File(...)):
    upnews = await file.read()
    return  upnews #name file or link

