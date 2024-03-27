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

import schemas.slurmer_cluster as schemas
import repository.slurmer_cluster as repo

router = APIRouter(
    prefix="/slurmer_clusters",
    tags=["SlurmerCluster"],
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


# admin
@router.get("/admin", response_model=list[schemas.SlurmerClusterAdmin])
async def admin_get_slurmer_cluster(db: Session = Depends(get_db)):
    return repo.get_slurmer_cluster_list(db)


@router.put("/admin", response_model=schemas.SlurmerClusterCreate)
async def admin_create_slurmer_cluster(
    create: schemas.PackageCreate,
    auth: AuthDep,
    db: Session = Depends(get_db),
):
    slurmer_cluster = repo.create(db, create)
    if slurmer_cluster:
        return slurmer_cluster
    raise HTTPException(404, "slurmer_cluster not found")


@router.get("/admin/{id}", response_model=schemas.SlurmerClusterAdmin)  # list
async def admin_get_slurmer_cluster_by_id(id: int, db: Session = Depends(get_db)):
    slurmer_cluster = repo.get_slurmer_cluster(db, id)
    if slurmer_cluster:
        return slurmer_cluster
    raise HTTPException(404, "slurmer_cluster not found")


@router.patch("/admin/{id}", response_model=schemas.SlurmerClusterSave)
async def admin_update_slurmer_cluster(
    id: int,
    save: schemas.SlurmerClusterSave,
    db: Session = Depends(get_db),
):
    slurmer_cluster = repo.get_slurmer_cluster(db, id)
    if slurmer_cluster:
        save.id = id
        return repo.save(db, save)
    raise HTTPException(404, "slurmer_cluster not found")
