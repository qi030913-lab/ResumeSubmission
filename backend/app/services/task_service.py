from datetime import UTC, datetime
from uuid import uuid4

from app.schemas.tasks import TaskCreate, TaskRead, TaskStatus


class TaskService:
    def __init__(self) -> None:
        self._tasks: dict[str, TaskRead] = {}

    def list_tasks(self) -> list[TaskRead]:
        return sorted(self._tasks.values(), key=lambda item: item.created_at, reverse=True)

    def create_task(self, payload: TaskCreate) -> TaskRead:
        now = datetime.now(UTC)
        task = TaskRead(
            id=str(uuid4()),
            status=TaskStatus.QUEUED,
            created_at=now,
            updated_at=now,
            **payload.model_dump(),
        )
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> TaskRead | None:
        return self._tasks.get(task_id)

    def update_status(self, task_id: str, status: TaskStatus) -> TaskRead | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None

        updated = task.model_copy(update={"status": status, "updated_at": datetime.now(UTC)})
        self._tasks[task_id] = updated
        return updated


task_service = TaskService()

