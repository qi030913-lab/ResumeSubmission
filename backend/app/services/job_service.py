from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import Job
from app.schemas.jobs import JobCreate


class JobService:
    def list_jobs(self, session: Session, platform_code: str | None = None) -> list[Job]:
        stmt = select(Job).order_by(Job.created_at.desc())
        if platform_code:
            stmt = stmt.where(Job.platform_code == platform_code)
        return list(session.scalars(stmt))

    def get_job(self, session: Session, job_id: str) -> Job | None:
        return session.get(Job, job_id)

    def create_job(self, session: Session, payload: JobCreate) -> Job:
        job = Job(**payload.model_dump())
        session.add(job)
        session.commit()
        session.refresh(job)
        return job


job_service = JobService()

