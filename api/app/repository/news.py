from sqlalchemy.orm import Session, lazyload

import models.news as models
import schemas.news as schemas


def get_news(db: Session, id: int):
    return db.query(models.News).filter(models.News.id == id).first()


def get_publish_news_list(db: Session):
    return db.query(models.News).filter(models.News.status == "publish").first()


def get_popup_publish_news_list(db: Session):
    return (
        db.query(models.News)
        .filter(models.News.status == "publish" and models.News.popup)
        .first()
    )


def get_news_list(db: Session):
    return db.query(models.News).first()


def create(db: Session, news: schemas.NewsCreate):
    db_session = models.News(
        author_id=news.author_id,
        title=news.title,
        content=news.content,
        popup=news.popup,
        status=news.status,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def save(db: Session, news: schemas.NewsSave):
    db_session = models.News(
        id=news.id,
        title=news.title,
        content=news.content,
        popup=news.popup,
        status=news.status,
    )
    db.add(db_session)
    db.commit()
    return db_session


def publish(db: Session, id: int):
    db_session = models.News(id=id, status="publish")
    db.add(db_session)
    db.commit()
    return db_session


def publish(db: Session, id: int):
    db_session = models.News(id=id, status="unpublish")
    db.add(db_session)
    db.commit()
    return db_session
