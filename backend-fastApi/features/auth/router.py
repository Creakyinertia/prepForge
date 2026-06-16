from fastapi import APIRouter, Depends, Response, Cookie
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from core.database import get_db
from core.exceptions import AppError, to_http_exception, InvalidRefreshTokenError
from dependencies.auth import get_current_user
from features.auth.schema import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserResponse,
)
from features.auth.service import AuthService
from core.config import settings
from models.user import User

router = APIRouter(tags=["Auth"])

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
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        result = auth_service.login(
            db,
            payload.email,
            payload.password,
        )

        response.set_cookie(
            key="refresh_token",
            value=result["refresh_token"],
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=(settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60),
        )

        return {
            "access_token": result["access_token"],
            "token_type": result["token_type"],
        }

    except AppError as exc:
        raise to_http_exception(exc) from exc


# only for testing with swagger, will be removed later
@router.post("/token")
def token_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    try:
        return auth_service.login(
            db=db, email=form_data.username, password=form_data.password
        )
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    try:
        if not refresh_token:
            raise InvalidRefreshTokenError()

        result = auth_service.refresh_access_token(
            db,
            refresh_token,
        )

        response.set_cookie(
            key="refresh_token",
            value=result["refresh_token"],
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=(settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60),
        )

        return {
            "access_token": result["access_token"],
            "token_type": result["token_type"],
        }

    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.post("/logout")
def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if refresh_token:
        auth_service.logout(
            db,
            refresh_token,
        )

    response.delete_cookie("refresh_token")

    return {"message": "Logged out"}


@router.get(
    "/me",
    response_model=UserResponse,
)
def me(current_user: User = Depends(get_current_user)):
    return current_user
