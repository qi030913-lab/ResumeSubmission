from fastapi import APIRouter, HTTPException, status

from app.db.session import SessionDep
from app.schemas.profiles import CandidateProfileCreate, CandidateProfileRead
from app.services.profile_service import profile_service

router = APIRouter()


@router.get("", response_model=list[CandidateProfileRead])
def list_profiles(session: SessionDep) -> list[CandidateProfileRead]:
    return [CandidateProfileRead.model_validate(item) for item in profile_service.list_profiles(session)]


@router.post("", response_model=CandidateProfileRead, status_code=status.HTTP_201_CREATED)
def create_profile(payload: CandidateProfileCreate, session: SessionDep) -> CandidateProfileRead:
    profile = profile_service.create_profile(session, payload)
    return CandidateProfileRead.model_validate(profile)


@router.get("/{profile_id}", response_model=CandidateProfileRead)
def get_profile(profile_id: str, session: SessionDep) -> CandidateProfileRead:
    profile = profile_service.get_profile(session, profile_id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return CandidateProfileRead.model_validate(profile)

