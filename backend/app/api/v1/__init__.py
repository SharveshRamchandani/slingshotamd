from fastapi import APIRouter
from .auth import router as auth_router
from .ingestion import router as ingestion_router
from .tasks import router as tasks_router
from .schedule import router as schedule_router
from .notifications import router as notifications_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(ingestion_router, prefix="/ingestion", tags=["ingestion"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
api_router.include_router(schedule_router, prefix="/schedule", tags=["schedule"])
api_router.include_router(notifications_router, prefix="/notifications", tags=["notifications"])
