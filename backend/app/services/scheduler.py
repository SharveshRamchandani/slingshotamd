from app.models.postgres_models import Task
from typing import List

def generate_schedule(tasks: List[Task], user_availability: float):
    """
    Generate optimized study schedules.
    Tasks should be sorted by priority.
    """
    sorted_tasks = sorted(tasks, key=lambda x: x.priority_score, reverse=True)
    
    schedule = []
    current_time_slot = 0.0
    
    for task in sorted_tasks:
        if current_time_slot >= user_availability:
            break
            
        time_to_allocate = task.estimated_study_time
        if time_to_allocate <= 0:
            time_to_allocate = 1.0 # default
            
        if current_time_slot + time_to_allocate > user_availability:
            # allocate remaining time
            allocated = user_availability - current_time_slot
        else:
            allocated = time_to_allocate
            
        schedule.append({
            "task_id": task.task_id,
            "title": task.title,
            "allocated_hours": round(allocated, 2),
            "priority": task.priority_score
        })
        current_time_slot += allocated
        
    return {
        "schedule": schedule,
        "total_allocated_hours": round(current_time_slot, 2),
        "available_hours": user_availability
    }
