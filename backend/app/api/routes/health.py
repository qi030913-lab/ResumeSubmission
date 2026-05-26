from fastapi import APIRouter
from sqlalchemy import text

from app.core.config import get_settings
from app.db.session import SessionDep
from app.schemas.common import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check(session: SessionDep) -> HealthResponse:
    settings = get_settings()
    session.execute(text("SELECT 1"))
    return HealthResponse(status="ok", service=settings.app_name, database="ok")


@router.get("/ready", response_model=HealthResponse)
def readiness_check(session: SessionDep) -> HealthResponse:
    settings = get_settings()
    session.execute(text("SELECT 1"))
    return HealthResponse(status="ok", service=settings.app_name, database="ok")
