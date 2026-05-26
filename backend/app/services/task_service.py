from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import ApplicationTask, CandidateProfile, Device, Job, MessageTemplate
from app.schemas.tasks import TaskCreate, TaskStatus


class TaskService:
    def list_tasks(self, session: Session, status: TaskStatus | None = None) -> list[ApplicationTask]:
        stmt = select(ApplicationTask).order_by(ApplicationTask.created_at.desc())
        if status is not None:
            stmt = stmt.where(ApplicationTask.status == status.value)
        return list(session.scalars(stmt))

    def get_task(self, session: Session, task_id: str) -> ApplicationTask | None:
        return session.get(ApplicationTask, task_id)

    def create_task(self, session: Session, payload: TaskCreate) -> ApplicationTask:
        self._validate_relations(session, payload)
        now = datetime.now(UTC)
        task = ApplicationTask(
            **payload.model_dump(),
            status=TaskStatus.QUEUED.value,
            scheduled_at=now,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    def update_status(
        self,
        session: Session,
        task_id: str,
        status: TaskStatus,
        error_message: str | None = None,
    ) -> ApplicationTask | None:
        task = session.get(ApplicationTask, task_id)
        if task is None:
            return None

        task.status = status.value
        task.error_message = error_message
        task.updated_at = datetime.now(UTC)
        session.commit()
        session.refresh(task)
        return task

    def attach_worker_job_id(self, session: Session, task_id: str, worker_job_id: str) -> ApplicationTask | None:
        task = session.get(ApplicationTask, task_id)
        if task is None:
            return None
        task.worker_job_id = worker_job_id
        task.dispatched_at = datetime.now(UTC)
        session.commit()
        session.refresh(task)
        return task

    def _validate_relations(self, session: Session, payload: TaskCreate) -> None:
        if session.get(Job, payload.job_id) is None:
            raise ValueError("Job not found")
        if session.get(Device, payload.device_id) is None:
            raise ValueError("Device not found")
        if session.get(CandidateProfile, payload.profile_id) is None:
            raise ValueError("Profile not found")
        if payload.message_template_id and session.get(MessageTemplate, payload.message_template_id) is None:
            raise ValueError("Message template not found")


task_service = TaskService()

