from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
import hashlib
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.connections.database import get_db
from backend.models.usermodel import User,RefreshToken
from sqlalchemy.orm import Session

SECRET_KEY = "f0200c7311b8938f5ff502b6f535cf4f4e10f3a82f9075eebef7ad19610a9c8b"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30



def hash_token(token: str) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()



def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )



def create_access_token(data: dict):
    
    payload = data.copy()
    payload["type"] = "access"
    payload["exp"] = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    acces_token_data = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    expiry_date = payload["exp"] 
    return acces_token_data,expiry_date


def create_refresh_token(data: dict):
    
    payload = data.copy()
    payload["type"] = "refresh"
    payload["exp"] = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )
    refresh_token_data = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    expiry_date = payload["exp"] 
    return refresh_token_data,expiry_date




def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # if payload.get("type") != "refresh":
        #     raise ValueError("Invalid token type")

        return payload

    except ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail="Refresh token has expired"
        )

    except InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to decode refresh token: {str(e)}"
        )
        


security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    print(token)
    
    token_hash = hash_token(
        token
    )

    db_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token_hash == token_hash
        )
        .first()
    )
    if db_token:
        if db_token.revoked_at:
              raise HTTPException(
            status_code=401,
            detail="Session expired"
        )
            
    
    payload = decode_refresh_token(token)

    username = payload["sub"]

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid user"
        )

    active_refresh = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.user_id == user.id
        )
        .first()
    )

    if not active_refresh:
        raise HTTPException(
            status_code=401,
            detail="Session expired"
        )

    return username