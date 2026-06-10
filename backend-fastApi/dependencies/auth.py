from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
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
        user_id=payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user = db.get(User, user_id)
        if not user:
           raise HTTPException(
               status_code=401,
               detail="User not found",
           )

        return user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )