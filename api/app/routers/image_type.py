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

import schemas.image_type as schemas
import repository.image_type as repo

router = APIRouter(
    prefix="/image-types",
    tags=["Image Types"],
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


@router.get("", response_model=list[schemas.ImageType])
async def get_image_type(db: Session = Depends(get_db)):
    return repo.get_image_type_list(db)


# admin
@router.get("/admin", response_model=list[schemas.ImageTypeAdmin])
async def admin_get_image_type(db: Session = Depends(get_db)):
    return repo.get_image_type_list(db)


@router.put("/admin", response_model=schemas.ImageType)
async def admin_create_image_type(
    create: schemas.ImageTypeCreate,
    auth: AuthDep,
    db: Session = Depends(get_db),
):
    image_type = repo.create(db, create)
    if image_type:
        return image_type
    raise HTTPException(404)


@router.get("/admin/{id}", response_model=schemas.ImageType)  # list
async def admin_get_image_type_by_id(id: int, db: Session = Depends(get_db)):
    image_type = repo.get_image_type(db, id)
    if image_type:
        return image_type
    raise HTTPException(404)


@router.patch("/admin/{id}", response_model=schemas.ImageType)
async def admin_update_image_type(
    id: int, save: schemas.ImageTypeSave, db: Session = Depends(get_db)
):
    image_type = repo.get_image_type(db, id)
    if image_type:
        save.id = id
        return repo.save(db, save)
    raise HTTPException(404)
