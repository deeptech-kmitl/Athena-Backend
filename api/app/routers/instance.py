from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Info(BaseModel):
    title: str
    status: str

info_data = [
    Info(title="jin", status="Active"),
    Info(title="joe", status="Inactive"),
]

@router.get("/info/{id}", response_model=Info)
async def get_info(id: int):
    if id < 1 or id > len(info_data):
        raise HTTPException(status_code=404, detail="Info not found")
    return info_data[id - 1]

@router.get("/info", response_model=List[Info])
async def get_all_info():
    return info_data

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
