from pydantic import BaseModel

from schemas.image import Image
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
    images: list[Image]

    class Config:
        orm_mode = True


class ImageTypeAdmin(ImageTypeBase):
    id: int
    images: list[Image]

    class Config:
        orm_mode = True
