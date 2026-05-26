from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.bootstrap import seed_reference_data
from app.core.config import get_settings
from app.db.session import SessionLocal, init_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_database()
    if get_settings().database_seed_reference_data:
        with SessionLocal() as session:
            seed_reference_data(session)
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        openapi_url="/api/v1/openapi.json",
        lifespan=lifespan,
    )
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
