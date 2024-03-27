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

import schemas.image as schemas
import repository.image as repo
import repository.image_type as imageTypeRepo

router = APIRouter(
    prefix="/images",
    tags=["Images"],
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


@router.get("", response_model=list[schemas.Image])
async def get_image(db: Session = Depends(get_db)):
    return repo.get_image_list(db)


# admin
@router.get("/admin", response_model=list[schemas.ImageAdmin])
async def admin_get_image(db: Session = Depends(get_db)):
    return repo.get_image_list(db)


@router.put("/admin", response_model=schemas.Image)
async def admin_create_image(
    create: schemas.ImageCreate,
    auth: AuthDep,
    db: Session = Depends(get_db),
):
    if imageTypeRepo.get_image_type(db, create.type_id) is None:
        raise HTTPException(404, "image type not found")
    image = repo.create(db, create)
    if image:
        return image
    raise HTTPException(404, "image not found")


@router.get("/admin/{id}", response_model=schemas.Image)  # list
async def admin_get_image_by_id(id: int, db: Session = Depends(get_db)):
    image = repo.get_image(db, id)
    if image:
        return image
    raise HTTPException(404, "image not found")


@router.patch("/admin/{id}", response_model=schemas.Image)
async def admin_update_image(
    id: int, image_save: schemas.ImageSave, db: Session = Depends(get_db)
):
    if imageTypeRepo.get_image_type(db, image_save.type_id) is None:
        raise HTTPException(404, "image type not found")
    image = repo.get_image(db, id)
    if image:
        image_save.id = id
        return repo.save(db, image_save)
    raise HTTPException(404, "image not found")
