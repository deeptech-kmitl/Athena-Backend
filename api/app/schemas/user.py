from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class SessionBase(BaseModel):
    pass


class SessionCreate(SessionBase):
    user_id: int
    user_agent: str


class SessionSave(SessionBase):
    pass
