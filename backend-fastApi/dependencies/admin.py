from fastapi import Depends
from core.exceptions import (
    AuthorizationError,
    to_http_exception,
)

from dependencies.auth import (
    get_current_user,
)


def get_current_admin(
    current_user=Depends(
        get_current_user
    ),
):
    if not current_user.is_admin:
        raise to_http_exception(
            AuthorizationError(
                "Admin access required"
            )
        )

    return current_user
