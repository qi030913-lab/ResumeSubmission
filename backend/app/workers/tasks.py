from uuid import uuid4

from app.workers.celery_app import celery_app


def enqueue_task(task_id: str) -> str:
    async_result = execute_application_task.delay(task_id)
    return str(async_result.id)


@celery_app.task(name="execute_application_task")
def execute_application_task(task_id: str) -> dict:
    # Real execution will load the task from database and choose the proper adapter.
    return {
        "job_id": str(uuid4()),
        "task_id": task_id,
        "result": "accepted_by_worker",
    }

