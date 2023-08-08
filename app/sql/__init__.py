from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config import sql_settings, sql_session_settings

engine = create_engine(
    sql_settings.url,
    # NOTE: If we use multithread, we could use this args too:
    # connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, **(sql_session_settings.model_dump()))

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()