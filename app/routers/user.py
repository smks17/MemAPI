from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    Token
)
from ..sql import get_db
from ..sql.schemas import User, UserCreate
from ..sql.crud import get_user, create_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def signup(
    form_data: Annotated[UserCreate, Depends()]
):
    user = get_user(get_db(), form_data.username)
    if user is not None:
        if user.email == form_data.email:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="This account is already exist!",
            )
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="This username is already exist!",
        )
    new_user = UserCreate(username=form_data.username,
                          email=form_data.email,
                          password=form_data.password)
    create_user(get_db(), new_user)
    return {"message": "Your account has been created successfully!"}

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    data = {"username": user.username}
    access_token = create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user