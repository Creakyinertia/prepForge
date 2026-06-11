from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from core.database import get_db

from dependencies.auth import (
    get_current_user,
)

from features.home.schema import (
    HomeResponse,
)

from features.home.service import (
    HomeService,
)

from models.user import User


router = APIRouter()

home_service = HomeService()


@router.get(
    "",
    response_model=HomeResponse,
)
def get_home(
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    return home_service.get_home_data(
        db,
        current_user.id,
    )