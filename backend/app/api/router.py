from fastapi import APIRouter

from app.api.routes import health, platforms, tasks

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(platforms.router, prefix="/platforms", tags=["platforms"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

