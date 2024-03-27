from sqlalchemy.orm import Session, lazyload

import models.package as models
import schemas.package as schemas


def get_package(db: Session, id: int):
    return db.query(models.Package).filter(models.Package.id == id).first()


def get_package_list(db: Session):
    return db.query(models.Package).all()


def create(db: Session, package: schemas.PackageCreate):
    db_session = models.Package(
        name=package.name,
        image_url=package.image_url,
        gres=package.gres,
        cpu=package.cpu,
        gpu=package.gpu,
        memory=package.memory,
        storage=package.storage,
        price=package.price,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def save(db: Session, save: schemas.PackageSave):
    package = db.query(models.Package).filter(models.Package.id == save.id).first()
    if package:
        package.name = save.name
        package.image_url = save.image_url
        package.cpu = save.cpu
        package.gpu = save.gpu
        package.memory = save.memory
        package.storage = save.storage
        package.price = save.price
        package.gres = save.gres
        db.commit()
        db.refresh(package)
    return package
