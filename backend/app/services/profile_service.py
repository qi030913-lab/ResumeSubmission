from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import CandidateProfile
from app.schemas.profiles import CandidateProfileCreate


class CandidateProfileService:
    def list_profiles(self, session: Session) -> list[CandidateProfile]:
        stmt = select(CandidateProfile).order_by(CandidateProfile.created_at.desc())
        return list(session.scalars(stmt))

    def get_profile(self, session: Session, profile_id: str) -> CandidateProfile | None:
        return session.get(CandidateProfile, profile_id)

    def create_profile(self, session: Session, payload: CandidateProfileCreate) -> CandidateProfile:
        profile = CandidateProfile(**payload.model_dump())
        session.add(profile)
        session.commit()
        session.refresh(profile)
        return profile


profile_service = CandidateProfileService()

