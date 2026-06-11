from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from core.database import get_db
from core.exceptions import (
    AppError,
    to_http_exception,
)
from dependencies.auth import get_current_user

from features.auth.schema import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    LogoutRequest,
    TokenResponse,
    UserResponse,
)
from features.auth.service import AuthService

from models.user import User

router = APIRouter(
    tags=["Auth"]
)

auth_service = AuthService()

@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    try:
        return auth_service.register(
            db,
            payload.email,
            payload.username,
            payload.password,
        )
    except AppError as exc:
        raise to_http_exception(exc) from exc

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        return auth_service.login(
            db,
            payload.email,
            payload.password,
        )
    except AppError as exc:
        raise to_http_exception(exc) from exc
#only for testing with swagger, will be removed later
@router.post("/token")
def token_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        return auth_service.login(
            db=db,
            email=form_data.username,
            password=form_data.password
        )
    except AppError as exc:
        raise to_http_exception(exc) from exc

@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh(
    payload: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    try:
        return auth_service.refresh_access_token(
            db,
            payload.refresh_token,
        )
    except AppError as exc:
        raise to_http_exception(exc) from exc

@router.post("/logout")
def logout(
    payload: LogoutRequest,
    db: Session = Depends(get_db),
):
    auth_service.logout(
        db,
        payload.refresh_token,
    )

    return {
        "message": "Logged out"
    }

@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(
        get_current_user
    )
):
    return current_user
