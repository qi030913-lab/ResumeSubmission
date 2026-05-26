from fastapi import APIRouter, HTTPException, status

from app.schemas.tasks import (
    TaskCreate,
    TaskDispatchResponse,
    TaskRead,
    TaskStatusUpdate,
)
from app.services.task_service import task_service
from app.workers.tasks import enqueue_task

router = APIRouter()


@router.get("", response_model=list[TaskRead])
def list_tasks() -> list[TaskRead]:
    return task_service.list_tasks()


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> TaskRead:
    return task_service.create_task(payload)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: str) -> TaskRead:
    task = task_service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("/{task_id}/dispatch", response_model=TaskDispatchResponse)
def dispatch_task(task_id: str) -> TaskDispatchResponse:
    task = task_service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    job_id = enqueue_task(task_id)
    return TaskDispatchResponse(task_id=task_id, celery_job_id=job_id, status="queued")


@router.patch("/{task_id}/status", response_model=TaskRead)
def update_task_status(task_id: str, payload: TaskStatusUpdate) -> TaskRead:
    task = task_service.update_status(task_id, payload.status)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

