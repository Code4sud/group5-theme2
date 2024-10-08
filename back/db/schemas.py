from pydantic import BaseModel
from typing import Optional, List  

class SimpleUser(BaseModel):
    name: str
    city: str

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None  

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = [] 

    class Config:
        orm_mode = True
