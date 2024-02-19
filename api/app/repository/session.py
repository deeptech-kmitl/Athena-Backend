from sqlalchemy.orm import Session, lazyload

import models.user as models
import schemas.user as schemas


def get_session(db: Session, id: int):
    return db.query(models.Session).filter(models.Session.id == id).first()


def create_session(db: Session, session: schemas.SessionCreate):
    db_session = models.Session(
        user_id=session.user_id,
        user_agent=session.user_agent,
        # csrf_token=session.csrf_token,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def save_session(db: Session, session: schemas.SessionSave):
    db_session = models.Session(user_id=session.user_id, is_revoke=session.is_revoke)
    db.add(db_session)
    db.commit()
    return db_session
