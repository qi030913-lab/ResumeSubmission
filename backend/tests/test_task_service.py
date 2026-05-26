from app.execution.task_executor import TaskExecutor
from app.models.base import Base
from app.models.entities import ApplicationTask, CandidateProfile, Device, DedupeRecord, Job, MessageTemplate
from app.schemas.tasks import TaskActionType, TaskCreate, TaskStatus
from app.services.task_service import TaskService
from app.db.session import create_engine_from_url

from sqlalchemy.orm import Session, sessionmaker


def build_session_factory() -> sessionmaker[Session]:
    engine = create_engine_from_url("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=Session)


def seed_required_records(session: Session) -> dict[str, str]:
    profile = CandidateProfile(name="默认简历")
    device = Device(device_code="pixel7-local", platform_type="android_app", device_name="Pixel 7")
    job = Job(platform_code="boss_android", title="Java 后端实习生", company_name="思维律动", recruiter_id="recruiter-1")
    template = MessageTemplate(
        platform_code="boss_android",
        scene_code="start_chat",
        title="默认首句",
        template_text="您好，我对{{job_title}}很感兴趣，最快{{availability_date}}到岗。",
    )
    session.add_all([profile, device, job, template])
    session.commit()
    return {
        "profile_id": profile.id,
        "device_id": device.id,
        "job_id": job.id,
        "template_id": template.id,
    }


def test_create_task_defaults_to_queued() -> None:
    session_factory = build_session_factory()
    service = TaskService()

    with session_factory() as session:
        ids = seed_required_records(session)
        task = service.create_task(
            session,
            TaskCreate(
                platform_code="boss_android",
                platform_type="android_app",
                action_type=TaskActionType.START_CHAT,
                job_id=ids["job_id"],
                device_id=ids["device_id"],
                profile_id=ids["profile_id"],
                message_template_id=ids["template_id"],
            ),
        )

        assert task.status == TaskStatus.QUEUED.value
        assert task.payload == {}


def test_task_executor_runs_start_chat_flow() -> None:
    session_factory = build_session_factory()
    service = TaskService()

    with session_factory() as session:
        ids = seed_required_records(session)
        task = service.create_task(
            session,
            TaskCreate(
                platform_code="boss_android",
                platform_type="android_app",
                action_type=TaskActionType.START_CHAT,
                job_id=ids["job_id"],
                device_id=ids["device_id"],
                profile_id=ids["profile_id"],
                message_template_id=ids["template_id"],
            ),
        )

    result = TaskExecutor(session_factory).execute(task.id)

    assert result["status"] == TaskStatus.SUCCEEDED.value

    with session_factory() as session:
        db_task = session.get(ApplicationTask, task.id)
        dedupe = session.query(DedupeRecord).all()

        assert db_task is not None
        assert db_task.status == TaskStatus.SUCCEEDED.value
        assert len(db_task.runs) == 1
        assert db_task.runs[0].result == "succeeded"
        assert db_task.runs[0].raw_output["steps"][1]["action"] == "start_chat"
        assert len(db_task.runs[0].raw_output["steps"]) == 2
        assert not any(
            operation["action"] == "type_text" for operation in db_task.runs[0].raw_output["driver_operations"]
        )
        assert len(dedupe) == 1
