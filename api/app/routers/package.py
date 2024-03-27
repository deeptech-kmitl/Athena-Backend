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

import schemas.package as schemas
import repository.package as repo

router = APIRouter(
    prefix="/packages",
    tags=["Packages"],
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


@router.get("", response_model=list[schemas.Package])
async def get_package(db: Session = Depends(get_db)):
    return repo.get_package_list(db)


# admin
@router.get("/admin", response_model=list[schemas.PackageAdmin])
async def admin_get_package(db: Session = Depends(get_db)):
    return repo.get_package_list(db)


@router.put("/admin", response_model=schemas.Package)
async def admin_create_package(
    create: schemas.PackageCreate,
    auth: AuthDep,
    db: Session = Depends(get_db),
):
    package = repo.create(db, create)
    if package:
        return package
    raise HTTPException(404, "package not found")


@router.get("/admin/{id}", response_model=schemas.Package)  # list
async def admin_get_package_by_id(id: int, db: Session = Depends(get_db)):
    package = repo.get_package(db, id)
    if package:
        return package
    raise HTTPException(404, "package not found")


@router.patch("/admin/{id}", response_model=schemas.Package)
async def admin_update_package(
    id: int, package_save: schemas.PackageSave, db: Session = Depends(get_db)
):
    package = repo.get_package(db, id)
    if package:
        package_save.id = id
        return repo.save(db, package_save)
    raise HTTPException(404, "package not found")
