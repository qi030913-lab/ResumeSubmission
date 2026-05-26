from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel


class ApplicationRunRead(ORMModel):
    id: str
    task_id: str
    driver_type: str
    adapter_code: str
    started_at: datetime
    finished_at: datetime | None = None
    result: str
    error_code: str | None = None
    error_message: str | None = None
    screenshot_urls: list = Field(default_factory=list)
    trace_url: str | None = None
    raw_output: dict = Field(default_factory=dict)
