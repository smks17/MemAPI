import datetime
from hashlib import sha256

from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, username: str) -> schemas.User:
    """get user from database by username"""
    q = db.query(models.User).filter(models.User.username == username)
    return q.first()

def get_user_by_email(db: Session, email: str) -> schemas.User:
    """get user from database by email"""
    q = db.query(models.User).filter(models.User.email == email)
    return q.first()

def create_user(db: Session, user: schemas.UserCreate):
    """create user and insert to database"""
    hashed_password = sha256((user.password).encode()).digest()
    db_user = models.User(username=user.username,
                          email=user.email,
                          password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_mem(db: Session, limit: int = 5) -> schemas.ListOfMemory:
    """Returns last n memory usage that were logged"""
    q = db.query(models.Memory)
    mem_data = q.limit(limit).all()
    mem_data = [schemas.Memory(**(mem.__dict__)) for mem in mem_data]
    return schemas.ListOfMemory(mem_data=mem_data)

def create_memory(db: Session, memory: schemas.MemCreate):
    """create memory and insert to database"""
    time = datetime.datetime.utcnow()
    db_mem = models.Memory(time=time, **(memory.dict()))
    db.add(db_mem)
    db.commit()
    db.refresh(db_mem)
    return db_mem
