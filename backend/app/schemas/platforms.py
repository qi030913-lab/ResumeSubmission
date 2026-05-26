from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel


class PlatformBase(ORMModel):
    platform_code: str = Field(..., examples=["boss_android"])
    platform_name: str = Field(..., examples=["Boss 直聘 Android"])
    platform_family: str = Field(..., examples=["boss"])
    platform_type: str = Field(..., examples=["android_app"])
    adapter_code: str = Field(..., examples=["boss_android_adapter"])
    is_active: bool = True
    health_status: str = "healthy"
    supported_actions: list[str] = Field(default_factory=list)


class PlatformCreate(PlatformBase):
    pass


class PlatformRead(PlatformBase):
    id: str
    last_verified_at: datetime | None = None
