from typing import Optional
from dotenv import dotenv_values
from pydantic import BaseModel, validator

config = dotenv_values(".env")

LAB_DOMAIN = config["LAB_DOMAIN"]


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
    url: Optional[str] | None = None

    @validator("url", pre=True, always=True)
    def make_c(cls, v: str, values: dict):
        return (
            "https://"
            + LAB_DOMAIN
            + "/lab/"
            + values["tunnel_id"]
            + "?token="
            + values["token"]
        )

    class Config:
        from_attributes = True


class InstanceAdmin(InstanceBase):
    id: int
    name: str
    status: str

    tunnel_id: str
    token: str
    local_port: int
    remote_port: int

    package_id: int
    image_id: int
    slurmer_id: int

    owner_id: int

    class Config:
        from_attributes = True
