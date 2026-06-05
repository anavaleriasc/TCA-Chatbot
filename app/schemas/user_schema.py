from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email:Optional[str] = None
    password:Optional[str] = None

class UserPublic(BaseModel):
    id:int
    email:str
    data_cadastro:datetime
  

    class Config:
        from_attributes=True



