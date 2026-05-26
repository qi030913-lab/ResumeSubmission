from fastapi import APIRouter, HTTPException, Query, status

from app.db.session import SessionDep
from app.schemas.message_templates import MessageTemplateCreate, MessageTemplateRead
from app.services.message_template_service import message_template_service

router = APIRouter()


@router.get("", response_model=list[MessageTemplateRead])
def list_templates(
    session: SessionDep,
    platform_code: str | None = Query(default=None),
) -> list[MessageTemplateRead]:
    templates = message_template_service.list_templates(session, platform_code)
    return [MessageTemplateRead.model_validate(item) for item in templates]


@router.post("", response_model=MessageTemplateRead, status_code=status.HTTP_201_CREATED)
def create_template(payload: MessageTemplateCreate, session: SessionDep) -> MessageTemplateRead:
    template = message_template_service.create_template(session, payload)
    return MessageTemplateRead.model_validate(template)


@router.get("/{template_id}", response_model=MessageTemplateRead)
def get_template(template_id: str, session: SessionDep) -> MessageTemplateRead:
    template = message_template_service.get_template(session, template_id)
    if template is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message template not found")
    return MessageTemplateRead.model_validate(template)

