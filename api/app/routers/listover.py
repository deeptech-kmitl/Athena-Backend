from fastapi import FastAPI, HTTPException, status, Query
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ListItem(BaseModel):
    title: str
    status: str

watchlist = [
    ListItem(title="list 1", status="To Watch"),
    ListItem(title="list 2", status="To Watch"),
    ListItem(title="list 3", status="To Watch"),
]

@router.get("/watchlist/", response_model=List[ListItem])
async def getlist():
    return watchlist

@router.get("/watchlist/filter/", response_model=List[ListItem])
async def getlist(status: str = Query(None, title="Filter by status")):
    if status:
        filter = [item for item in watchlist if item.status == status]
        return filter
    return watchlist

app = FastAPI()
app.include_router(router)
