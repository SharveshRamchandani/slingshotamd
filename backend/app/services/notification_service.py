import logging

logger = logging.getLogger(__name__)

async def send_deadline_alert(user_id: int, task_title: str, deadline: str):
    logger.info(f"[ALERT] User {user_id}: Upcoming deadline for {task_title} at {deadline}")

async def send_new_announcement_alert(user_id: int, title: str):
    logger.info(f"[ALERT] User {user_id}: New announcement - {title}")

async def send_study_session_alert(user_id: int, session_start: str, task_title: str):
    logger.info(f"[ALERT] User {user_id}: Study session for {task_title} starts at {session_start}")
