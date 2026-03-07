from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.services.notification_service import send_deadline_alert
from pydantic import BaseModel

class AlertRequest(BaseModel):
    task_title: str
    deadline: str

router = APIRouter()

@router.post("/test-alert")
async def trigger_test_alert(
    request: AlertRequest,
    current_user: int = Depends(get_current_user)
):
    await send_deadline_alert(current_user, request.task_title, request.deadline)
    return {"status": "Alert sent"}
