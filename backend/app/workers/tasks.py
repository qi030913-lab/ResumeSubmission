from app.db.session import SessionLocal
from app.execution.task_executor import TaskExecutor
from app.workers.celery_app import celery_app

task_executor = TaskExecutor(SessionLocal)


def enqueue_task(task_id: str) -> str:
    async_result = execute_application_task.delay(task_id)
    return str(async_result.id)


@celery_app.task(name="execute_application_task")
def execute_application_task(task_id: str) -> dict:
    return task_executor.execute(task_id)
