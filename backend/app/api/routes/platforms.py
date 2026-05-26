from fastapi import APIRouter, HTTPException, status

from app.schemas.platforms import PlatformCreate, PlatformRead
from app.services.platform_service import platform_service

router = APIRouter()


@router.get("", response_model=list[PlatformRead])
def list_platforms() -> list[PlatformRead]:
    return platform_service.list_platforms()


@router.get("/{platform_code}", response_model=PlatformRead)
def get_platform(platform_code: str) -> PlatformRead:
    platform = platform_service.get_platform(platform_code)
    if platform is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Platform not found")
    return platform


@router.post("", response_model=PlatformRead, status_code=status.HTTP_201_CREATED)
def create_platform(payload: PlatformCreate) -> PlatformRead:
    return platform_service.create_platform(payload)

