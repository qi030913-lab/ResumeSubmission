from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import Field

from app.schemas.common import ORMModel


class TaskStatus(StrEnum):
    DRAFT = "draft"
    QUEUED = "queued"
    RUNNING = "running"
    WAITING_MANUAL_REVIEW = "waiting_manual_review"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED_DUPLICATE = "skipped_duplicate"


class TaskActionType(StrEnum):
    START_CHAT = "start_chat"
    SEND_RESUME = "send_resume"
    SUBMIT_APPLICATION = "submit_application"
    FOLLOW_UP_CHAT = "follow_up_chat"


class TaskCreate(ORMModel):
    platform_code: str = Field(..., examples=["boss_android"])
    platform_type: str = Field(..., examples=["android_app"])
    action_type: TaskActionType
    job_id: str
    device_id: str
    profile_id: str
    message_template_id: str | None = None
    requires_manual_review: bool = True
    priority: int = 0
    payload: dict[str, Any] = Field(default_factory=dict)


class TaskRead(ORMModel):
    id: str
    platform_code: str
    platform_type: str
    action_type: TaskActionType
    job_id: str
    device_id: str
    profile_id: str
    message_template_id: str | None = None
    requires_manual_review: bool
    priority: int
    payload: dict[str, Any] = Field(default_factory=dict)
    worker_job_id: str | None = None
    error_message: str | None = None
    status: TaskStatus
    dispatched_at: datetime | None = None
    scheduled_at: datetime
    created_at: datetime
    updated_at: datetime


class TaskStatusUpdate(ORMModel):
    status: TaskStatus
    error_message: str | None = None


class TaskDispatchResponse(ORMModel):
    task_id: str
    celery_job_id: str
    dispatch_status: str
    task_status: TaskStatus

