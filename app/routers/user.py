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
from ..sql.crud import get_user, get_user_by_email, create_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register",
             status_code=status.HTTP_201_CREATED,
             responses = {
                201: {"message": "Your account has been created successfully!"},
                406: {"detail": "This username is already exist!"}
             }
            )
async def signup(
    form_data: Annotated[UserCreate, Depends()]
):
    """Signing up and creating a new user.
    
    Parameters
    ---------
    form_data: UserCreate
        User information should contain a username, email and password. It should be
        passed from params.

    Return
    ------
    Dict[str, str]
        It returns a JSON with status code HTTP201 and contains a message. If username
        or email has already existed, it will return a message with code HTTP406 and
        detail.

    Note
    ----
        Actually, this function shouldn't exist for this specific API and an admin should
        add and access users. But for now and for tests it is here.
    """
    # TODO: The password should pass from user in hashed.
    # check user or username has already exited or not
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
    user = get_user_by_email(get_db(), form_data.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="This account is already exist!",
        )
    # TODO: It should check email
    new_user = UserCreate(username=form_data.username,
                          email=form_data.email,
                          password=form_data.password)
    create_user(get_db(), new_user)
    return {"message": "Your account has been created successfully!"}

@router.post("/token",
             status_code=status.HTTP_201_CREATED,
             responses = {
                201: {"model": Token},
                401: {"detail": "Incorrect username or password"}
             })
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """Logging up and creating a new token to work with the API. First, you should register.
    (see /users/register)
    
    Parameters
    ---------
    form_data: OAuth2PasswordRequestForm
        User information should contain a username and password. The user should exist.
        It should be passed from body.

    Return
    ------
    Dict[str, str]
        It returns a JSON with status code HTTP201 and contains a "access_token" and
        "token_type. If username or email does not exist, it will return a message
        with code HTTP401 and detail.
    """
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

@router.get("/me",
             status_code=status.HTTP_200_OK,
             response_model=User,
             responses = {
                400: {"detail": "Inactive user"}
             })
async def check_token(current_user: Annotated[User, Depends(get_current_active_user)]):
    """Checking a token and return user of token. First, you should login and get a token.
    (see /users/token)

    Parameters
    ----------
    current_user
        This function requires a token. It should be passed a Bearer token type that
        got from API. See Also: /users/token
    """
    return current_user