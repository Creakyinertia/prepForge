from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from enum import Enum


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, description="Must contain at least 8 characters")
    confirm_password: str

    @model_validator(mode="after")
    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
    
    






class CountryCode(str, Enum):
    INDIA = "+91"
    USA = "+1"
    UK = "+44"
    UAE = "+971"
    AUSTRALIA = "+61"


class UserProfileCreate(BaseModel):
    first_name: str
    last_name: str
    country_code: str = Field(pattern=r"^\+\d{1,4}$")
    phone: str
    bio: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None