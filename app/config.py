import datetime
from typing import Dict

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    class Info(BaseSettings):
        """Configs to use metadata"""
        title: str = "Memory Api"
        summary: str = "A simple api for get information about system memory."
        contact: Dict[str, str] = {
            "name": "Mahdi Kashani",
            "email": "m.kashani1381@gmail.com",
        }

    class Sql(BaseSettings):
        """Configs to use in sql"""
        url: str = "sqlite:///./sql_app.sqlite"
        class Session(BaseSettings):
            autocommit: bool = False
            autoflush: bool = False

    class Token(BaseSettings):
        """Configs to use in token creation and validation"""
        # Your secret key to generate token for users
        secret_key: str = "Mahdi Kashani"
        # algorithm to use in token creation
        algorithm: str = "HS256"
        # time in which is valid
        access_token_expire_minutes: datetime.timedelta = datetime.timedelta(minutes=30)

    # debug mode or not
    debug: bool = True
    # delta time to sleep between each memory checking.
    delta_time_check_memory: datetime.timedelta = datetime.timedelta(minutes=1)


settings = AppSettings()
info_settings = settings.Info()
sql_settings = settings.Sql()
sql_session_settings = sql_settings.Session()
token_settings = settings.Token()