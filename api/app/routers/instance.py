import binascii
import os
import random
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from services.kong import create_route, create_service
from services.mole import create_alias, open_tunnel
from services.slurmer import start_job, submit_job
from middleware.auth import get_auth_user, AuthDep
from database.engine import SessionLocal
from sqlalchemy import Column, Integer, String, Boolean

import schemas.instance as schemas
import repository.instance as repo

import schemas.package as packageSchemas
import repository.package as packageRepo
import schemas.image as imageSchemas
import repository.image as imageRepo
import schemas.slurmer_cluster as slurmerClusterSchemas
import repository.slurmer_cluster as slurmerClusterRepo
import schemas.user as userSchemas
import repository.user as userRepo

router = APIRouter(
    prefix="/instances",
    tags=["Instances"],
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


@router.get("", response_model=list[schemas.Instance])
async def get_instance(db: Session = Depends(get_db)):
    return repo.get_instance_list(db)


@router.post("/rent", response_model=schemas.Instance)
async def admin_create_instance(
    create: schemas.InstanceCreate,
    auth: AuthDep,
    db: Session = Depends(get_db),
):
    package = packageRepo.get_package(db, create.package_id)
    if package is None:
        raise HTTPException(404, "package not found")
    image = imageRepo.get_image(db, create.image_id)
    if image is None:
        raise HTTPException(404, "image not found")

    slurmer_list = slurmerClusterRepo.get_slurmer_cluster_list(db)

    if len(slurmer_list) < 1:
        raise HTTPException(500, "cluster not ready")

    slurmer = slurmer_list[0]  # Select first

    remote_port = slurmer.random_port()
    local_port = random.randint(4000, 6000)

    instance = repo.create(
        db,
        create,
        owner_id=auth.user.id,
        tunnel_id=uuid.uuid4().hex,
        token=binascii.hexlify(os.urandom(40)).decode(),
        local_port=local_port,
        remote_port=remote_port,
        slurmer_id=slurmer.id,
    )
    if instance:
        job = submit_job(slurmer, instance, image, package)
        job_id = job["id"]
        instance = repo.set_job(db, instance.id, job_id)
        start_job(slurmer, job_id)
        create_alias(
            instance.tunnel_id,
            local_port,
            slurmer.endpoint_server + ":" + str(remote_port),
            slurmer.server_proxy,
        )
        path = "/lab/" + instance.tunnel_id
        create_service(instance.tunnel_id, instance.local_port, path)
        create_route(instance.tunnel_id, path)
        open_tunnel(instance.tunnel_id)
        return instance
    raise HTTPException(404, "instance not found")


# admin
@router.get("/admin", response_model=list[schemas.InstanceAdmin])
async def admin_get_instance(db: Session = Depends(get_db)):
    return repo.get_instance_list(db)


@router.get("/admin/{id}", response_model=schemas.InstanceAdmin)  # list
async def admin_get_instance_by_id(id: int, db: Session = Depends(get_db)):
    instance = repo.get_instance(db, id)
    if instance:
        return instance
    raise HTTPException(404, "instance not found")


@router.get("/{id}", response_model=schemas.Instance)
async def get_instance_by_id(id: int, db: Session = Depends(get_db)):
    instance = repo.get_instance(db, id)
    if instance:
        return instance
    raise HTTPException(404)
