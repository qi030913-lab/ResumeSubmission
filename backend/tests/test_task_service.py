from app.schemas.tasks import TaskActionType, TaskCreate, TaskStatus
from app.services.task_service import TaskService


def test_create_task_defaults_to_queued() -> None:
    service = TaskService()
    task = service.create_task(
        TaskCreate(
            platform_code="boss_android",
            platform_type="android_app",
            action_type=TaskActionType.START_CHAT,
            job_id="job-1",
            device_id="device-1",
            profile_id="profile-1",
            payload={"send_greeting": True},
        )
    )

    assert task.status == TaskStatus.QUEUED
    assert task.payload["send_greeting"] is True
