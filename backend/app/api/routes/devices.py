from fastapi import APIRouter, HTTPException, status

from app.db.session import SessionDep
from app.schemas.devices import DeviceCreate, DeviceRead
from app.services.device_service import device_service

router = APIRouter()


@router.get("", response_model=list[DeviceRead])
def list_devices(session: SessionDep) -> list[DeviceRead]:
    return [DeviceRead.model_validate(item) for item in device_service.list_devices(session)]


@router.post("", response_model=DeviceRead, status_code=status.HTTP_201_CREATED)
def create_device(payload: DeviceCreate, session: SessionDep) -> DeviceRead:
    device = device_service.create_device(session, payload)
    return DeviceRead.model_validate(device)


@router.get("/{device_id}", response_model=DeviceRead)
def get_device(device_id: str, session: SessionDep) -> DeviceRead:
    device = device_service.get_device(session, device_id)
    if device is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    return DeviceRead.model_validate(device)

