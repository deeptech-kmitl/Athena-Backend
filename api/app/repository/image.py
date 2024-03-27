from sqlalchemy.orm import Session, lazyload

import models.image as models
import schemas.image as schemas


def get_image(db: Session, id: int):
    return db.query(models.Image).filter(models.Image.id == id).first()


def get_image_list(db: Session):
    return db.query(models.Image).all()


def create(db: Session, image: schemas.ImageCreate):
    db_session = models.Image(
        name=image.name,
        image_url=image.image_url,
        squashfs_location=image.squashfs_location,
        type_id=image.type_id,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def save(db: Session, save: schemas.ImageSave):
    image = db.query(models.Image).filter(models.Image.id == save.id).first()
    if image:
        image.name = save.name
        image.image_url = save.image_url
        image.squashfs_location = save.squashfs_location
        image.type_id = save.type_id
        db.commit()
        db.refresh(image)
    return image
