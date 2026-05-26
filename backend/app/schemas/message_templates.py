from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel


class MessageTemplateBase(ORMModel):
    platform_code: str = Field(..., examples=["boss_android"])
    scene_code: str = Field(..., examples=["start_chat"])
    title: str
    template_text: str
    variables: list[str] = Field(default_factory=list)
    is_active: bool = True


class MessageTemplateCreate(MessageTemplateBase):
    pass


class MessageTemplateRead(MessageTemplateBase):
    id: str
    created_at: datetime
    updated_at: datetime
