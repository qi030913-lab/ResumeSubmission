from fastapi import APIRouter, HTTPException, Query, status

from app.db.session import SessionDep
from app.schemas.tasks import TaskCreate, TaskDispatchResponse, TaskRead, TaskStatus, TaskStatusUpdate
from app.services.task_service import task_service
from app.workers.tasks import enqueue_task

router = APIRouter()


@router.get("", response_model=list[TaskRead])
def list_tasks(session: SessionDep, status: TaskStatus | None = Query(default=None)) -> list[TaskRead]:
    tasks = task_service.list_tasks(session, status)
    return [TaskRead.model_validate(task) for task in tasks]


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, session: SessionDep) -> TaskRead:
    try:
        task = task_service.create_task(session, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return TaskRead.model_validate(task)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: str, session: SessionDep) -> TaskRead:
    task = task_service.get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskRead.model_validate(task)


@router.post("/{task_id}/dispatch", response_model=TaskDispatchResponse)
def dispatch_task(task_id: str, session: SessionDep) -> TaskDispatchResponse:
    task = task_service.get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    job_id = enqueue_task(task_id)
    task = task_service.attach_worker_job_id(session, task_id, job_id)
    assert task is not None
    return TaskDispatchResponse(
        task_id=task_id,
        celery_job_id=job_id,
        dispatch_status="dispatched",
        task_status=TaskStatus(task.status),
    )


@router.patch("/{task_id}/status", response_model=TaskRead)
def update_task_status(task_id: str, payload: TaskStatusUpdate, session: SessionDep) -> TaskRead:
    task = task_service.update_status(session, task_id, payload.status, payload.error_message)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskRead.model_validate(task)

