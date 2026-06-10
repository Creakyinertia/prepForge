from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.connections.database import get_db
from backend.models.usermodel import User,RefreshToken
from backend.schemas.userschema import UserRegister, UserLogin,RefreshTokenRequest
from backend.core.security import ( 
                                   hash_password,
                                   verify_password,
                                   create_refresh_token,
                                   hash_token,
                                   decode_refresh_token,
                                   get_current_user,
                                   create_access_token)
from sqlalchemy import or_
from datetime import datetime
from fastapi import Header

router = APIRouter(
    prefix="/v1",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    payload: UserRegister,
    db: Session = Depends(get_db)
):
    passwd = hash_password(payload.password)
    existing_user = (
    db.query(User)
    .filter(
        or_(
            User.email == payload.email,
            User.username == payload.username
        )
    )
    .first()
)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    passwd= hash_password(
            payload.password
        )
    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=passwd
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    raise HTTPException(
    status_code=200,
    detail={"message": "User registered successfully"})
    
    
    
@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = (
        db.query(User)
        .filter(
            (User.username == user.username) |
            (User.email == user.username)
        )
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )
    access_token, access_expiry = create_access_token({"sub": db_user.username})
    refresh_token, refresh_expiry = create_refresh_token(
        {"sub": db_user.username}
    )

    refresh_token_hash = hash_token(
        refresh_token
    )

    existing_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.user_id == db_user.id
        )
        .first()
    )

    if existing_token:

        existing_token.token_hash = refresh_token_hash
        existing_token.expires_at = refresh_expiry
        existing_token.revoked_at = None

    else:

        new_token = RefreshToken(
            user_id=db_user.id,
            token_hash=refresh_token_hash,
            expires_at=refresh_expiry
        )

        db.add(new_token)

    db.commit()

    return {
        "access_token":access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "access_expires_at":access_expiry.isoformat(),
        "refresh_expires_at": refresh_expiry.isoformat()
    }
    

@router.post("/refresh")
def refresh_tokens(
    token: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    
    payload = decode_refresh_token(
        token.refresh_token
    )

    token_hash = hash_token(
        token.refresh_token
    )

    db_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token_hash == token_hash
        )
        .first()
    )
    

    if not db_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )
    


    username = payload["sub"]

    access_token, access_expiry = create_access_token({"sub": username})
    refresh_token, refresh_expiry = (
        create_refresh_token(
            {"sub": username}
        )
    )

    if db_token:
        db_token.token_hash = hash_token(refresh_token)
        db_token.expires_at = access_expiry
    else:
        db.add(
            RefreshToken(
                user_id=db_token.id,
                token_hash=hash_token(refresh_token),
                expires_at=access_expiry
            )
        )

    db.commit()

    return {
        "access_token":access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "access_expires_at":access_expiry.isoformat(),
        "refresh_expires_at": refresh_expiry.isoformat()
    }
    

@router.delete("/logout")
def logout(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.username == current_user)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    logout_user  = db.query(RefreshToken).filter(
            RefreshToken.user_id == user.id).first()
    logout_user.revoked_at = (datetime.now()).isoformat()

    db.commit()

    return {
        "message": "Logged out successfully"
    }
