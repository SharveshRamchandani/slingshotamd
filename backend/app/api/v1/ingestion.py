from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.core.database import get_mongo_db
from app.workers.tasks import process_ingested_message_task
from pydantic import BaseModel

class WebhookPayload(BaseModel):
    message: str
    source: str

router = APIRouter()

@router.post("/webhook")
async def ingest_webhook(
    payload: WebhookPayload,
    current_user: int = Depends(get_current_user),
    mongo_db = Depends(get_mongo_db)
):
    """
    Simulated webhook. Saves to MongoDB then queues a Celery task 
    for NLP extraction & priority calculation.
    """
    raw_col = mongo_db["raw_messages"]
    doc = {
        "user_id": current_user,
        "source": payload.source,
        "message": payload.message,
        "processed": False
    }
    await raw_col.insert_one(doc)
    
    # Send to Celery
    task = process_ingested_message_task.delay(payload.message, current_user)
    
    return {"status": "Processing in background", "task_id": str(task.id)}

@router.post("/sync/gmail")
async def sync_gmail(current_user: int = Depends(get_current_user)):
    # Trigger gmail ingestion connector here
    return {"status": "Syncing gmail data for user..."}
