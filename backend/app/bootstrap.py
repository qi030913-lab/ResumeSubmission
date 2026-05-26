from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import PlatformRegistry


def seed_reference_data(session: Session) -> None:
    platform = session.scalar(
        select(PlatformRegistry).where(PlatformRegistry.platform_code == "boss_android")
    )
    if platform is None:
        session.add(
            PlatformRegistry(
                platform_code="boss_android",
                platform_name="Boss 直聘 Android",
                platform_family="boss",
                platform_type="android_app",
                adapter_code="boss_android_adapter",
                health_status="healthy",
                supported_actions=["open_job", "start_chat", "send_greeting", "send_resume"],
                last_verified_at=datetime.now(UTC),
            )
        )
        session.commit()

