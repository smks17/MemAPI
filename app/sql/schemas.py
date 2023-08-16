from datetime import datetime
from typing import List

from pydantic import BaseModel


class MemBase(BaseModel):
    free: float
    used: float
    total: float


class MemCreate(MemBase):
    time: datetime


class Memory(MemCreate):
    class Config:
        orm_mode = True


class ListOfMemory(BaseModel):
    """contains a list of memory for query"""
    mem_data: List[Memory]


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    activated: bool

    class Config:
        orm_mode = True
