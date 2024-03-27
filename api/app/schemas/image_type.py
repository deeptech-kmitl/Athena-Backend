from pydantic import BaseModel
from . import user


class ImageTypeBase(BaseModel):
    name: str
    image_url: str


class ImageTypeCreate(ImageTypeBase):
    pass


class ImageTypeSave(ImageTypeCreate):
    id: int | None = None


class ImageType(ImageTypeBase):
    id: int

    class Config:
        orm_mode = True


class ImageTypeAdmin(ImageTypeBase):
    id: int

    class Config:
        orm_mode = True
