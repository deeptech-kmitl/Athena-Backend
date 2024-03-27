from sqlalchemy.orm import Session, lazyload

import models.image_type as models
import schemas.image_type as schemas


def get_image_type(db: Session, id: int):
    return db.query(models.ImageType).filter(models.ImageType.id == id).first()


def get_image_type_list(db: Session):
    return db.query(models.ImageType).all()


def create(db: Session, image_type: schemas.ImageTypeCreate):
    db_session = models.ImageType(
        name=image_type.name,
        image_url=image_type.image_url,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def save(db: Session, save: schemas.ImageTypeSave):
    image_type = (
        db.query(models.ImageType).filter(models.ImageType.id == save.id).first()
    )
    if image_type:
        image_type.name = save.name
        image_type.image_url = save.image_url
        db.commit()
        db.refresh(image_type)
    return image_type
