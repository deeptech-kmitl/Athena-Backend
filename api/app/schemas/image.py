from pydantic import BaseModel
from . import user


class ImageBase(BaseModel):
    name: str
    image_url: str


class ImageCreate(ImageBase):
    pass


class ImageSave(ImageBase):
    id: int
    squashfs_location: str


class Image(ImageBase):
    id: int

    class Config:
        orm_mode = True


class ImageAdmin(ImageBase):
    id: int
    squashfs_location: str

    class Config:
        orm_mode = True
