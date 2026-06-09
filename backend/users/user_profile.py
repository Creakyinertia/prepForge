from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.connections.database import get_db
from backend.models.usermodel import User,RefreshToken
from backend.schemas.userschema import UserRegister, UserLogin
from backend.core.security import ( 
                                   hash_password,
                                   verify_password,
                                   create_refresh_token,
                                   hash_token,
                                   decode_refresh_token,
                                   get_current_user,
                                   create_access_token)
from sqlalchemy import or_
from fastapi import UploadFile, File, Form


router = APIRouter(
    prefix="/v1",
    tags=["UserProfile"]
)


@router.get("/profile")
def profile(
    current_user: str = Depends(
        get_current_user
    )
):
    print(current_user)
    return {
        "message": "Authorized",
        "user": current_user
    }

@router.post("/profile")
async def create_profile(
    current_user: str = Depends(get_current_user),
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
    bio: str | None = Form(None),
    resume: UploadFile | None = File(None)
    ):
    if current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return {"data":"data"}


