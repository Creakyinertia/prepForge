from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from dependencies.auth import (
    get_current_user,
)
from features.dashboard.schema import (
    DashboardResponse,
)
from features.dashboard.service import (
    DashboardService,
)
from models.user import User

router = APIRouter()
dashboard_service = DashboardService()

@router.get(
    "",
    response_model=DashboardResponse,
)
def get_dashboard(
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    return dashboard_service.get_dashboard(
        db,
        current_user.id,
    )