from pydantic import BaseModel


class SlurmerClusterBase(BaseModel):
    name: str
    url: str
    token: str
    user: str
    start_port: int
    end_port: int
    app_id: str
    server_proxy: str
    endpoint_server: str


class SlurmerClusterCreate(SlurmerClusterBase):
    pass


class SlurmerClusterSave(SlurmerClusterBase):
    id: int | None = None


class SlurmerClusterAdmin(SlurmerClusterBase):
    id: int

    class Config:
        from_attributes = True
