from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.adapters.registry import adapter_registry
from app.execution.message_rendering import render_message_template
from app.models.entities import (
    ApplicationLog,
    ApplicationRun,
    ApplicationTask,
    CandidateProfile,
    DedupeRecord,
    Device,
    Job,
    MessageTemplate,
)
from app.schemas.tasks import TaskActionType, TaskStatus


class TaskExecutor:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def execute(self, task_id: str) -> dict:
        return asyncio.run(self._execute(task_id))

    async def _execute(self, task_id: str) -> dict:
        with self.session_factory() as session:
            task = session.get(ApplicationTask, task_id)
            if task is None:
                return {"task_id": task_id, "status": "not_found"}

            duplicate = self._find_duplicate(session, task)
            if duplicate is not None:
                task.status = TaskStatus.SKIPPED_DUPLICATE.value
                task.error_message = "Duplicate contact detected"
                session.add(
                    ApplicationLog(
                        task_id=task.id,
                        level="warn",
                        event_type="duplicate_detected",
                        message="Task skipped because a dedupe record already exists",
                        details={"dedupe_key": duplicate.dedupe_key},
                    )
                )
                session.commit()
                return {"task_id": task.id, "status": task.status}

            job = session.get(Job, task.job_id)
            device = session.get(Device, task.device_id)
            profile = session.get(CandidateProfile, task.profile_id)
            template = session.get(MessageTemplate, task.message_template_id) if task.message_template_id else None
            assert job is not None
            assert device is not None
            assert profile is not None
            adapter, driver = adapter_registry.build(task.platform_code, task.platform_type, device=device)

            task.status = TaskStatus.RUNNING.value
            task.error_message = None
            run = ApplicationRun(task_id=task.id, driver_type=driver.driver_type, adapter_code=adapter.platform_code)
            session.add(run)
            session.add(
                ApplicationLog(
                    task_id=task.id,
                    run=run,
                    event_type="task_started",
                    message=f"Started task {task.id}",
                    details={"action_type": task.action_type},
                )
            )
            session.commit()
            session.refresh(run)

            outputs: list[dict] = []
            screenshot_urls: list[str] = []
            try:
                outputs.append({"screen": await adapter.detect_screen()})
                if task.action_type == TaskActionType.START_CHAT.value:
                    outputs.append(await adapter.start_chat())
                    if task.payload.get("send_greeting", True):
                        message = render_message_template(template, job, profile)
                        outputs.append(await adapter.send_greeting(message))
                elif task.action_type == TaskActionType.SEND_RESUME.value:
                    outputs.append(await adapter.send_resume(task.payload.get("resume_id", "default-resume")))
                else:
                    outputs.append({"action": task.action_type, "status": "not_implemented"})

                screenshot_urls.append(await driver.take_screenshot())
                run.finished_at = datetime.now(UTC)
                run.result = "succeeded"
                run.screenshot_urls = screenshot_urls
                run.raw_output = {"steps": outputs, "driver_operations": driver.export_debug_trace()}
                task.status = TaskStatus.SUCCEEDED.value
                session.add(
                    ApplicationLog(
                        task_id=task.id,
                        run_id=run.id,
                        event_type="task_finished",
                        message=f"Finished task {task.id}",
                        details={"result": run.result},
                    )
                )
                session.add(
                    DedupeRecord(
                        platform_code=task.platform_code,
                        recruiter_id=job.recruiter_id,
                        job_id=job.id,
                        action_type=task.action_type,
                        dedupe_key=self._dedupe_key(task, job),
                        last_executed_at=datetime.now(UTC),
                    )
                )
                session.commit()
                return {"task_id": task.id, "status": task.status, "run_id": run.id}
            except Exception as exc:
                try:
                    screenshot_urls.append(await driver.take_screenshot())
                except Exception:
                    pass
                run.finished_at = datetime.now(UTC)
                run.result = "failed"
                run.error_code = exc.__class__.__name__
                run.error_message = str(exc)
                run.screenshot_urls = screenshot_urls
                run.raw_output = {"steps": outputs, "driver_operations": driver.export_debug_trace()}
                task.status = TaskStatus.FAILED.value
                task.error_message = str(exc)
                session.add(
                    ApplicationLog(
                        task_id=task.id,
                        run_id=run.id,
                        level="error",
                        event_type="task_failed",
                        message=f"Task {task.id} failed",
                        details={"error": str(exc), "error_code": exc.__class__.__name__},
                    )
                )
                session.commit()
                return {"task_id": task.id, "status": task.status, "run_id": run.id}
            finally:
                await driver.close()

    def _find_duplicate(self, session: Session, task: ApplicationTask) -> DedupeRecord | None:
        job = session.get(Job, task.job_id)
        assert job is not None
        stmt = select(DedupeRecord).where(DedupeRecord.dedupe_key == self._dedupe_key(task, job))
        return session.scalar(stmt)

    def _dedupe_key(self, task: ApplicationTask, job: Job) -> str:
        recruiter = job.recruiter_id or "unknown-recruiter"
        return f"{task.platform_code}:{recruiter}:{job.id}:{task.action_type}"
