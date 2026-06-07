from pydantic import BaseModel, EmailStr
from uuid import UUID

class RegisterRequest(
    BaseModel
):
    email: EmailStr
    username: str
    password: str

class LoginRequest(
    BaseModel
):
    email: str
    password: str

class TokenResponse(
    BaseModel
):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(
    BaseModel
):
    refresh_token: str

class LogoutRequest(
    BaseModel
):
    refresh_token: str

class UserResponse(
    BaseModel
):
    id: UUID
    email: str
    username: str

    model_config = {
        "from_attributes": True
    }