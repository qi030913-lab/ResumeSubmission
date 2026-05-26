from fastapi import APIRouter, HTTPException, Query, status

from app.db.session import SessionDep
from app.schemas.jobs import JobCreate, JobRead
from app.services.job_service import job_service

router = APIRouter()


@router.get("", response_model=list[JobRead])
def list_jobs(session: SessionDep, platform_code: str | None = Query(default=None)) -> list[JobRead]:
    return [JobRead.model_validate(item) for item in job_service.list_jobs(session, platform_code)]


@router.post("", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate, session: SessionDep) -> JobRead:
    job = job_service.create_job(session, payload)
    return JobRead.model_validate(job)


@router.get("/{job_id}", response_model=JobRead)
def get_job(job_id: str, session: SessionDep) -> JobRead:
    job = job_service.get_job(session, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return JobRead.model_validate(job)

