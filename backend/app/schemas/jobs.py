from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel


class JobBase(ORMModel):
    platform_code: str = Field(..., examples=["boss_android"])
    external_job_id: str | None = None
    title: str
    company_name: str
    city: str | None = None
    salary_text: str | None = None
    recruiter_name: str | None = None
    recruiter_id: str | None = None
    job_url: str | None = None
    job_snapshot: dict = Field(default_factory=dict)


class JobCreate(JobBase):
    pass


class JobRead(JobBase):
    id: str
    created_at: datetime
    updated_at: datetime
