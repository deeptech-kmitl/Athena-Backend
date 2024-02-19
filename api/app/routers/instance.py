from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
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
#   "Created At": "23 April 2309",
#   "Expied At": "25 April 2309",
  "Size": "Nano",
  "Type": "Juuu",
  "Sever": "DGX",
  "Location": "IT, Kmitl",
},{
  "ID": "test01",
  "Author": "64070000@it.kmitl.ac.th",
#   "Created At": "23 April 2309",
#   "Expied At": "25 April 2309",
  "Size": "Nano",
  "Type": "Juuu",
  "Sever": "DGX",
  "Location": "IT, Kmitl",
},
    
]

class Instance(BaseModel):
    ID: str
    Author: str
    # CreatedAt: str
    # ExpiedAt: str
    Size: str
    Type: str
    Sever: str
    Location: str
    
@router.get("/instance")
async def read_instance(instance_id: int) -> Instance:
    return instance_db[instance_id]
