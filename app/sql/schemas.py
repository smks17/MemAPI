from datetime import datetime
from typing import List

from pydantic import BaseModel


class MemBase(BaseModel):
    free: float
    used: float
    total: float


class MemCreate(MemBase):
    pass


class Memory(MemBase):
    time: datetime
    class Config:
        orm_mode = True


class ListOfMemory(BaseModel):
    """contains a list of memory for query"""
    mem_data: List[Memory]


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    email: str
    password: str


class User(UserBase):
    activated: bool

    class Config:
        orm_mode = True
