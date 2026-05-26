from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel


class DeviceBase(ORMModel):
    device_code: str = Field(..., examples=["pixel7-local"])
    platform_type: str = Field(..., examples=["android_app"])
    device_name: str = Field(..., examples=["Pixel 7"])
    adb_serial: str | None = Field(default=None, examples=["emulator-5554"])
    status: str = "idle"
    capabilities: dict = Field(default_factory=dict)


class DeviceCreate(DeviceBase):
    pass


class DeviceRead(DeviceBase):
    id: str
    last_seen_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
