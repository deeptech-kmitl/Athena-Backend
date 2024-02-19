from pydantic import BaseModel


class NewsBase(BaseModel):
    pass


class NewsCreate(NewsBase):
    user_id: int
    title: str
    connect: str
    popup: bool
    status: str


class NewsSave(BaseModel):
    id: int
    title: str
    connect: str
    popup: bool
    status: str


class News(BaseModel):
    id: int
    title: str
    connect: str
    popup: bool
    status: str

    class Config:
        orm_mode = True
