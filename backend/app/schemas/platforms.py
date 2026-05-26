from pydantic import BaseModel, Field


class PlatformBase(BaseModel):
    platform_code: str = Field(..., examples=["boss_android"])
    platform_name: str = Field(..., examples=["Boss 直聘 Android"])
    platform_family: str = Field(..., examples=["boss"])
    platform_type: str = Field(..., examples=["android_app"])
    adapter_code: str = Field(..., examples=["boss_android_adapter"])


class PlatformCreate(PlatformBase):
    pass


class PlatformRead(PlatformBase):
    health_status: str = "healthy"
    supported_actions: list[str] = []

