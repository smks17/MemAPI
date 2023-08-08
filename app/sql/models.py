from sqlalchemy import (
    Boolean,
    Column,
    Float,
    String,
    TIMESTAMP,
    VARCHAR
)

from . import Base

class User(Base):
    __tablename__ = "User"
    username = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(VARCHAR(64))  # store hashed password
    activated = Column(Boolean, default=True)


class Memory(Base):
    __tablename__ = "Memory"
    time = Column(TIMESTAMP, primary_key=True)
    free = Column(Float)
    used = Column(Float)
    total = Column(Float)