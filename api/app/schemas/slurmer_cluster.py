from pydantic import BaseModel


class SlurmerClusterBase(BaseModel):
    name: str


class SlurmerClusterCreate(SlurmerClusterBase):
    url: str
    token: str
    user: str
    start_port: int
    end_port: int


class SlurmerClusterSave(SlurmerClusterBase):
    id: int
    url: str
    token: str
    user: str
    start_port: int
    end_port: int


class SlurmerCluster(SlurmerClusterBase):
    id: int

    class Config:
        orm_mode = True


class SlurmerClusterAdmin(SlurmerClusterBase):
    id: int
    url: str
    token: str
    user: str
    start_port: int
    end_port: int

    class Config:
        orm_mode = True
