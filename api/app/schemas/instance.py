from pydantic import BaseModel


class InstanceBase(BaseModel):
    name: str
    assign_to: str | None = None


class InstanceCreate(InstanceBase):
    package_id: int
    image_id: int


class InstanceSave(InstanceBase):
    id: int | None = None


class Instance(InstanceBase):
    id: int

    tunnel_id: str
    token: str
    status: str

    class Config:
        orm_mode = True


class InstanceAdmin(InstanceBase):
    id: int
    name: str
    status: str

    tunnel_id: str
    token: str
    port: int
    map_to_port: int

    package_id: int
    image_id: int
    slurmer_id: int

    owner_id: int

    class Config:
        orm_mode = True
