from fastapi import APIRouter

from app.api.routes import devices, health, jobs, message_templates, platforms, profiles, runs, tasks

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(platforms.router, prefix="/platforms", tags=["platforms"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(message_templates.router, prefix="/message-templates", tags=["message-templates"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(runs.router, prefix="/runs", tags=["runs"])
