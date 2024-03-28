from pydantic import BaseModel
from . import user


class ImageBase(BaseModel):
    type_id: int
    name: str
    image_url: str


class ImageCreate(ImageBase):
    squashfs_location: str


class ImageSave(ImageCreate):
    id: int | None = None


class Image(ImageBase):
    id: int

    class Config:
        from_attributes = True


class ImageAdmin(ImageBase):
    id: int
    squashfs_location: str

    class Config:
        from_attributes = True
