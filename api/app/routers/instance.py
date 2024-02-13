from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import Annotated
from datetime import datetime, time, timedelta
# from fastapi.staticfiles import StaticFiles

router = APIRouter(
    prefix="/instance", 
    tags=["Instance"], 
    responses={404: {"message": "Not found"}}
)

instance_db = [
    {
  "ID": "JU-03",
  "Author": "64070000@it.kmitl.ac.th",
  "CreatedAt": "2008-09-15T15:53:00+05:00",
  "ExpiedAt": "2008-09-15T15:53:00+05:00",
  "Size": "Nano",
  "Type": "Juuu",
  "Sever": "DGX",
  "Location": "IT, Kmitl",
},{
  "ID": "test01",
  "Author": "64070000@it.kmitl.ac.th",
  "CreatedAt": "2008-09-15T15:53:00+05:00",
  "ExpiedAt": "2008-09-15T15:53:00+05:00",
  "Size": "Nano",
  "Type": "Juuu",
  "Sever": "DGX",
  "Location": "IT, Kmitl",
},
    
]

class Instance(BaseModel):
    ID: str
    Author: str
    CreatedAt: Annotated[datetime | None, Body()] = None,
    ExpiedAt: Annotated[datetime | None, Body()] = None,
    Size: str
    Type: str
    Sever: str
    Location: str
    
@router.get("/instance")
async def read_instance(instance_id: int) -> Instance:
    print(instance_db)
    return instance_db[instance_id]

@router.delete("/instance/{instance_id}")
async def delete_instance(instance_id: int):
    instance = instance_db.pop(instance_id)
    return instance

