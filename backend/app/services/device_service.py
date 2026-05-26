from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import Device
from app.schemas.devices import DeviceCreate


class DeviceService:
    def list_devices(self, session: Session) -> list[Device]:
        stmt = select(Device).order_by(Device.created_at.desc())
        return list(session.scalars(stmt))

    def get_device(self, session: Session, device_id: str) -> Device | None:
        return session.get(Device, device_id)

    def create_device(self, session: Session, payload: DeviceCreate) -> Device:
        device = Device(**payload.model_dump())
        session.add(device)
        session.commit()
        session.refresh(device)
        return device


device_service = DeviceService()

