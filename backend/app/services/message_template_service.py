from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import MessageTemplate
from app.schemas.message_templates import MessageTemplateCreate


class MessageTemplateService:
    def list_templates(self, session: Session, platform_code: str | None = None) -> list[MessageTemplate]:
        stmt = select(MessageTemplate).order_by(MessageTemplate.created_at.desc())
        if platform_code:
            stmt = stmt.where(MessageTemplate.platform_code == platform_code)
        return list(session.scalars(stmt))

    def get_template(self, session: Session, template_id: str) -> MessageTemplate | None:
        return session.get(MessageTemplate, template_id)

    def create_template(self, session: Session, payload: MessageTemplateCreate) -> MessageTemplate:
        template = MessageTemplate(**payload.model_dump())
        session.add(template)
        session.commit()
        session.refresh(template)
        return template


message_template_service = MessageTemplateService()

