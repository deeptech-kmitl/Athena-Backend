from sqlalchemy.orm import Session, lazyload

import models.instance as models
import schemas.instance as schemas


def get_instance(db: Session, id: int, user_id: int = None):
    query = db.query(models.Instance).filter(models.Instance.id == id)
    if user_id is not None:
        query = query.filter(models.Instance.owner_id == user_id)
    return query.first()


def get_instance_list(db: Session, user_id: int = None):
    query = db.query(models.Instance)
    if user_id is not None:
        query = query.filter(models.Instance.owner_id == user_id)
    return query.all()


def create(
    db: Session,
    instance: schemas.InstanceCreate,
    owner_id: int,
    tunnel_id: str,
    token: str,
    local_port: int,
    remote_port: int,
    slurmer_id: int,
):
    db_session = models.Instance(
        package_id=instance.package_id,
        image_id=instance.image_id,
        name=instance.name,
        assign_to=instance.assign_to,
        owner_id=owner_id,
        tunnel_id=tunnel_id,
        token=token,
        local_port=local_port,
        remote_port=remote_port,
        slurmer_id=slurmer_id,
        status="action",
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def save(db: Session, save: schemas.InstanceSave):
    instance = db.query(models.Instance).filter(models.Instance.id == save.id).first()
    if instance:
        instance.name = save.name
        instance.assign_to = save.assign_to
        db.commit()
        db.refresh(instance)
    return instance


def set_job(db: Session, id: int, job_id: str):
    instance = db.query(models.Instance).filter(models.Instance.id == id).first()
    if instance:
        instance.job_id = job_id
        db.commit()
        db.refresh(instance)
    return instance
