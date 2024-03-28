from sqlalchemy.orm import Session, lazyload

import models.instance as models
import schemas.instance as schemas


def get_instance(db: Session, id: int):
    return db.query(models.Instance).filter(models.Instance.id == id).first()


def get_instance_list(db: Session):
    return db.query(models.Instance).all()


def create(
    db: Session,
    instance: schemas.InstanceCreate,
    owner_id: int,
    tunnel_id: str,
    token: str,
    port: int,
    map_to_port: int,
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
        port=port,
        map_to_port=map_to_port,
        slurmer_id=slurmer_id,
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
