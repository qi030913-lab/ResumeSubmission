from fastapi import APIRouter, HTTPException, status

from app.db.session import SessionDep
from app.schemas.platforms import PlatformCreate, PlatformRead
from app.services.platform_service import platform_service

router = APIRouter()


@router.get("", response_model=list[PlatformRead])
def list_platforms(session: SessionDep) -> list[PlatformRead]:
    return [PlatformRead.model_validate(item) for item in platform_service.list_platforms(session)]


@router.get("/{platform_code}", response_model=PlatformRead)
def get_platform(platform_code: str, session: SessionDep) -> PlatformRead:
    platform = platform_service.get_platform(session, platform_code)
    if platform is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Platform not found")
    return PlatformRead.model_validate(platform)


@router.post("", response_model=PlatformRead, status_code=status.HTTP_201_CREATED)
def create_platform(payload: PlatformCreate, session: SessionDep) -> PlatformRead:
    platform = platform_service.create_platform(session, payload)
    return PlatformRead.model_validate(platform)

