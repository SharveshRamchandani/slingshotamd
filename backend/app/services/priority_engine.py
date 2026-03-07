from datetime import datetime, timezone
from app.models.postgres_models import Task

def calculate_priority_score(
    task_type: str, 
    deadline: datetime, 
    estimated_effort: float, 
    current_workload: int
) -> float:
    """
    Calculates priority score between 0 and 100 based on:
    - proximity to deadline
    - task type weight (exam > assignment > quiz > event)
    - estimated effort
    - user workload
    """
    
    type_weight = {
        "exam": 40,
        "assignment": 30,
        "quiz": 20,
        "event": 10
    }
    
    score = 0.0
    
    # 1. Type weight (0-40 points)
    score += type_weight.get(task_type.lower(), 10)
    
    # 2. Deadline proximity (0-40 points)
    if deadline:
        now = datetime.utcnow()
        if deadline.tzinfo:
            now = now.replace(tzinfo=timezone.utc)
            
        time_left = deadline - now
        days_left = max(0, time_left.days)
        
        # Exponential urgency for close deadlines
        if days_left <= 0:
            score += 40
        elif days_left <= 1:
            score += 35
        elif days_left <= 3:
            score += 25
        elif days_left <= 7:
            score += 15
        else:
            score += 5
            
    # 3. Estimated effort (0-10 points)
    if estimated_effort > 0:
        score += min(estimated_effort * 2, 10)

    # 4. User workload factor (0-10 points)
    if current_workload > 5:
        score += 10
    elif current_workload > 2:
        score += 5

    return min(100.0, max(0.0, score))
