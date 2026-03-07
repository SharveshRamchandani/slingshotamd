from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.postgres_models import TaskStatus

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority_score: Optional[float] = 0.0
    estimated_study_time: Optional[float] = 0.0
    status: Optional[TaskStatus] = TaskStatus.PENDING
    source: str

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    task_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ScheduleRequest(BaseModel):
    user_availability: float # available hours per day
