import secrets
from pwdlib import PasswordHash
import hashlib
from datetime import datetime, timezone, timedelta
import jwt
from core.config import settings

password_hash=PasswordHash.recommended()

def hash_password(password:str)->str:
    return password_hash.hash(password)

def verify_password(password:str, hashed_password:str)->bool:
    return password_hash.verify(password,hashed_password)

def create_access_token(user_id: str)->str:
    expire = (datetime.now(timezone.utc)+timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    ))

    payload = {
        "sub": user_id,
        "type": "access",
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

def decode_token(token:str):
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )

def generate_refresh_token()->str:
    return secrets.token_urlsafe(64)

def hash_refresh_token(token:str)->str:
    return hashlib.sha256(
        token.encode()
    ).hexdigest()