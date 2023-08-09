from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_db, get_current_active_user
from ..sql.schemas import ListOfMemory, User
from ..sql.crud import get_mem


router = APIRouter(prefix="/memory", tags=["memory"])

@router.get("/info/", response_model=ListOfMemory)
async def read_mem_info(current_user: Annotated[User, Depends(get_current_active_user)],
                        limit: int
) -> ListOfMemory:
    """It reads the last n memory information from database. First, you should login and
    get a token. (see /users/token)

    Parameters
    ----------
        current_user
            This function requires token. It should be pass a Bearer token type that
            got from API. See Also: /users/token
        limit:n
            how many gets from db. It should be passed as a param.

    Return
    ------
    ListOfMemory
        It returns list of memory information that have items: free, used, total, and time.
        See Also: `ListOfMemory`
    """
    mem = get_mem(get_db(), limit=int(limit))
    if not mem:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request",
        )
    return mem