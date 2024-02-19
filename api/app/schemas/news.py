from pydantic import BaseModel
from . import user


class NewsBase(BaseModel):
    pass


class NewsCreate(NewsBase):
    author_id: int = 0
    title: str
    content: str
    popup: bool
    status: str


class NewsSave(BaseModel):
    id: int
    title: str
    content: str
    popup: bool
    status: str


class News(BaseModel):
    id: int
    title: str
    content: str
    popup: bool
    status: str

    class Config:
        orm_mode = True


class NewsAdmin(BaseModel):
    id: int
    title: str
    content: str
    popup: bool
    status: str
    author_id: int
    author: user.User

    class Config:
        orm_mode = True
