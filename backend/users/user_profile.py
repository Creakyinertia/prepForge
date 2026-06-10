from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.connections.database import get_db
from backend.models.usermodel import User,RefreshToken,UserProfile
from backend.schemas.userschema import UserRegister, UserLogin,UserProfileCreate
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
import os
import shutil

router = APIRouter(
    prefix="/v1",
    tags=["UserProfile"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


ALLOWED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword"  
}

ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}


@router.post("/profile",status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile: UserProfileCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    user_db = db.query(User).filter(
        User.username == current_user).first()

    if profile:
        full_phone = f"{profile.country_code}{profile.phone}"
        profile_data = UserProfile(
            user_id = user_db.id,
            first_name = profile.first_name,
            last_name = profile.last_name,
            phone = full_phone,
            bio = profile.bio,
            linkedin_url = profile.linkedin_url,
            github_url = profile.github_url
        )

        db.add(profile_data)
        db.commit()
        db.refresh(profile_data)

    return {"data": profile_data}


@router.post("/upload-resume") 
async def upload_resume(
    resume: UploadFile | None = File(None),
):

    if not resume.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is missing"
        )

    extension = os.path.splitext(resume.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOC and DOCX files are allowed"
        )

    if resume.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type"
        )

    content = await resume.read()
    file_size_mb = f"{len(content) / (1024 * 1024):.2f}"
    max_size = "1"
    

    if file_size_mb > max_size:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 1 MB"
    )

    file_path = f"uploads/{resume.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    file_size = os.path.getsize(file_path)

    return {
        "filename": resume.filename,
        "size_bytes": f"{file_size_mb}MB",
        "path": file_path
    }