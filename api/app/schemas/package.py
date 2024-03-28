from pydantic import BaseModel
from . import user


class PackageBase(BaseModel):
    name: str
    cpu: int
    gpu: int
    memory: int
    storage: int
    image_url: str
    price: float


class PackageCreate(PackageBase):
    gres: str


class PackageSave(PackageCreate):
    id: int | None = None
    gres: str


class Package(PackageBase):
    id: int

    class Config:
        from_attributes = True


class PackageAdmin(PackageBase):
    id: int
    gres: str

    class Config:
        from_attributes = True
