from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.exceptions import (
    AuthenticationError,
    to_http_exception,
)
from core.security import decode_token
from models.user import User


# must be changed to /auth/login when not using swagger.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)

def get_current_user(
    token:str=Depends(oauth2_scheme),
    db:Session=Depends(get_db)
):
    try:
        payload=decode_token(token)
    except Exception as exc:
        raise to_http_exception(
            AuthenticationError("Invalid token")
        ) from exc

    user_id = payload.get("sub")
    if not user_id:
        raise to_http_exception(
            AuthenticationError("Invalid token")
        )

    user = db.get(User, user_id)
    if not user:
       raise to_http_exception(
           AuthenticationError("User not found")
       )

    return user
