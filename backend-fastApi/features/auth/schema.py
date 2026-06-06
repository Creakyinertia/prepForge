from pydantic import BaseModel, EmailStr

class RegisterRequest:
    email: EmailStr
    username: str
    password: str

class LoginRequest:
    email: str
    password: str

class TokenResponse:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"