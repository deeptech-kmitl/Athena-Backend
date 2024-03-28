from sqlalchemy.orm import Session, lazyload

import models.slurmer_cluster as models
import schemas.slurmer_cluster as schemas


def get_slurmer_cluster(db: Session, id: int):
    return (
        db.query(models.SlurmerCluster).filter(models.SlurmerCluster.id == id).first()
    )


def get_slurmer_cluster_list(db: Session):
    return db.query(models.SlurmerCluster).all()


def create(db: Session, slurmer_cluster: schemas.SlurmerClusterCreate):
    db_session = models.SlurmerCluster(
        name=slurmer_cluster.name,
        url=slurmer_cluster.url,
        app_id=slurmer_cluster.app_id,
        token=slurmer_cluster.token,
        user=slurmer_cluster.user,
        start_port=slurmer_cluster.start_port,
        end_port=slurmer_cluster.end_port,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def save(db: Session, save: schemas.SlurmerClusterSave):
    slurmer_cluster = (
        db.query(models.SlurmerCluster)
        .filter(models.SlurmerCluster.id == save.id)
        .first()
    )
    if slurmer_cluster:
        slurmer_cluster.name = save.name
        slurmer_cluster.url = save.url
        slurmer_cluster.app_id = save.app_id
        slurmer_cluster.token = save.token
        slurmer_cluster.user = save.user
        slurmer_cluster.start_port = save.start_port
        slurmer_cluster.end_port = save.end_port
        db.commit()
        db.refresh(slurmer_cluster)
    return slurmer_cluster
