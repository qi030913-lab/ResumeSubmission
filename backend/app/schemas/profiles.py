from datetime import date, datetime

from pydantic import Field

from app.schemas.common import ORMModel


class CandidateProfileBase(ORMModel):
    name: str = Field(..., examples=["默认简历"])
    headline: str | None = None
    base_info: dict = Field(default_factory=dict)
    availability_date: date | None = None
    preferred_roles: list[str] = Field(default_factory=list)


class CandidateProfileCreate(CandidateProfileBase):
    pass


class CandidateProfileRead(CandidateProfileBase):
    id: str
    created_at: datetime
    updated_at: datetime
