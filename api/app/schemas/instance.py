from pydantic import BaseModel


class InstanceBase(BaseModel):
    name: str


class InstanceCreate(InstanceBase):
    assign_to: str
    tunnel_instance_id: str
    port: int
    map_to_port: int
    package_id: int
    image_id: int
    slurmer_id: int
    owner_id: int


class InstanceSave(InstanceBase):
    id: int
    assign_to: str
    tunnel_instance_id: str


class Instance(InstanceBase):
    id: int
    assign_to: str

    class Config:
        orm_mode = True


class InstanceAdmin(InstanceBase):
    id: int
    assign_to: str
    tunnel_instance_id: str
    port: int
    map_to_port: int
    package_id: int
    image_id: int
    slurmer_id: int
    owner_id: int

    class Config:
        orm_mode = True
