from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import PlatformRegistry
from app.schemas.platforms import PlatformCreate


class PlatformService:
    def list_platforms(self, session: Session) -> list[PlatformRegistry]:
        stmt = select(PlatformRegistry).order_by(PlatformRegistry.platform_code.asc())
        return list(session.scalars(stmt))

    def get_platform(self, session: Session, platform_code: str) -> PlatformRegistry | None:
        stmt = select(PlatformRegistry).where(PlatformRegistry.platform_code == platform_code)
        return session.scalar(stmt)

    def create_platform(self, session: Session, payload: PlatformCreate) -> PlatformRegistry:
        platform = PlatformRegistry(
            **payload.model_dump(),
            last_verified_at=datetime.now(UTC),
        )
        session.add(platform)
        session.commit()
        session.refresh(platform)
        return platform


platform_service = PlatformService()

