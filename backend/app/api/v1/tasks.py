from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.task import TaskCreate, TaskResponse
from app.models.postgres_models import Task
from app.services.priority_engine import calculate_priority_score

router = APIRouter()

@router.post("/", response_model=TaskResponse)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    # Calculate priority
    score = calculate_priority_score(
        task_type="assignment", # dummy default type
        deadline=task_in.deadline,
        estimated_effort=task_in.estimated_study_time,
        current_workload=3 # dummy workload value
    )
    
    db_task = Task(
        user_id=current_user,
        title=task_in.title,
        description=task_in.description,
        deadline=task_in.deadline,
        priority_score=score,
        estimated_study_time=task_in.estimated_study_time,
        source=task_in.source,
        status=task_in.status
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    query = select(Task).where(Task.user_id == current_user).order_by(Task.priority_score.desc())
    result = await db.execute(query)
    return result.scalars().all()
