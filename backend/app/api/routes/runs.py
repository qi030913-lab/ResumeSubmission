from fastapi import APIRouter, HTTPException, Query, status

from app.db.session import SessionDep
from app.schemas.runs import ApplicationRunRead
from app.services.run_service import run_service

router = APIRouter()


@router.get("", response_model=list[ApplicationRunRead])
def list_runs(session: SessionDep, task_id: str | None = Query(default=None)) -> list[ApplicationRunRead]:
    runs = run_service.list_runs(session, task_id)
    return [ApplicationRunRead.model_validate(item) for item in runs]


@router.get("/{run_id}", response_model=ApplicationRunRead)
def get_run(run_id: str, session: SessionDep) -> ApplicationRunRead:
    run = run_service.get_run(session, run_id)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")
    return ApplicationRunRead.model_validate(run)
