from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.task import ScheduleRequest
from app.models.postgres_models import Task, TaskStatus
from app.services.scheduler import generate_schedule

router = APIRouter()

@router.post("/generate")
async def generate_user_schedule(
    request: ScheduleRequest,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    # Fetch pending tasks for the user
    query = select(Task).where(
        Task.user_id == current_user,
        Task.status == TaskStatus.PENDING
    )
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    # Generate schedule
    schedule = generate_schedule(tasks, request.user_availability)
    return schedule
