import datetime
from hashlib import sha256
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt

from .config import token_settings
from .sql import crud, schemas, get_db


class Token(BaseModel):
    """A simple class to store token information"""
    # the string of token that is usable for working
    access_token: str
    # specified type of token e.g "Bearer"
    token_type: str


class TokenData(BaseModel):
    """A simple class to be restored user by token"""
    username: Optional[str] = None
    email: Optional[str] = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    """Checks user sha256 passwords"""
    calculated_hash = (sha256(plain_password.encode()).digest())
    return (calculated_hash == hashed_password)

def authenticate_user(username: int, password: str) -> schemas.User:
    """Checks user has already existed or not and then check the user password. At the
    end return user object."""
    user = crud.get_user(get_db(), username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict,
                        expires_delta: Optional[datetime.timedelta]=None
) -> str:
    """create a token by user data.
    
    Parameters
    ----------
    data: dict
        The data that contains unique information like username.
    expires_delta: Optional[datetime.timedelta]=None
        The time in which the token is valid. If it's None, it will get from config.

    Return
    ------
    str
        The string of token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now() + expires_delta
    else:
        expire = datetime.datetime.now() + token_settings.access_token_expire_minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             token_settings.secret_key,
                             algorithm=token_settings.algorithm)
    return encoded_jwt

async def get_user_by_token(token: Annotated[str, Depends(oauth2_scheme)]) -> schemas.User:
    """Decode the user data from its token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,
                             token_settings.secret_key,
                             algorithms=[token_settings.algorithm])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.exceptions.PyJWTError:
        raise credentials_exception
    user = crud.get_user(get_db(), username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_user_by_token)]
):
    """Checks the user is active or not"""
    if not current_user.activated:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user