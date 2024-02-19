from sqlalchemy.orm import Session, lazyload

import models.news as models
import schemas.news as schemas


def get_news(db: Session, id: int):
    return db.query(models.News).filter(models.News.id == id).first()


def get_publish_news_list(db: Session):
    return db.query(models.News).filter(models.News.status == "publish").all()


def get_popup_publish_news_list(db: Session):
    return (
        db.query(models.News)
        .filter(models.News.status == "publish" and models.News.popup)
        .all()
    )


def get_news_list(db: Session):
    return db.query(models.News).all()


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


def save(db: Session, news_save: schemas.NewsSave):
    news = db.query(models.News).filter(models.News.id == news_save.id).first()
    if news:
        news.title = news_save.title
        news.content = news_save.content
        news.popup = news_save.popup
        news.status = news_save.status
        db.commit()
        db.refresh(news)
    return news


def publish(db: Session, id: int):
    news = db.query(models.News).filter(models.News.id == id).first()
    if news:
        news.status = "publish"
        db.commit()
        db.refresh(news)
    return news


def unpublish(db: Session, id: int):
    news = db.query(models.News).filter(models.News.id == id).first()
    if news:
        news.status = "draft"
        db.commit()
        db.refresh(news)
    return news
