from fastapi import Depends
from fastapi import HTTPException

from dependencies.auth import (
    get_current_user,
)


def get_current_admin(
    current_user=Depends(
        get_current_user
    ),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )

    return current_user