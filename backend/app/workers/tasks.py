from app.workers.celery_app import celery_app
from app.services.nlp_service import process_raw_message
import asyncio

# In a real app we would inject DB connections here
@celery_app.task(name="process_ingested_message")
def process_ingested_message_task(message_text: str, user_id: int):
    """
    Background worker that takes a raw ingested message,
    runs NLP extraction, and calculates priority.
    """
    extracted_data = process_raw_message(message_text)
    
    # Ideally, save to postgres here. We'll return it for demo purposes.
    return {
        "user_id": user_id,
        "structured_data": extracted_data
    }
