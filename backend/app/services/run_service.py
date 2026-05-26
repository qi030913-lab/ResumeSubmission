from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import ApplicationRun


class RunService:
    def list_runs(self, session: Session, task_id: str | None = None) -> list[ApplicationRun]:
        stmt = select(ApplicationRun).order_by(ApplicationRun.started_at.desc())
        if task_id:
            stmt = stmt.where(ApplicationRun.task_id == task_id)
        return list(session.scalars(stmt))

    def get_run(self, session: Session, run_id: str) -> ApplicationRun | None:
        return session.get(ApplicationRun, run_id)


run_service = RunService()

