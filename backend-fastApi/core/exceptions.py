from fastapi import HTTPException
from starlette import status


class AppError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad request"

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.default_detail
        super().__init__(self.detail)


class AuthenticationError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid credentials"


class AuthorizationError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Forbidden"


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Resource not found"


class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Resource already exists"


class UserAlreadyExistsError(ConflictError):
    default_detail = "User already exists"


class InvalidRefreshTokenError(AuthenticationError):
    default_detail = "Invalid refresh token"


def to_http_exception(error: AppError) -> HTTPException:
    return HTTPException(
        status_code=error.status_code,
        detail=error.detail,
    )
