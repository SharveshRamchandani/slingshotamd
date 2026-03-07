from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True) # allow null for oauth
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    google_id = Column(String, unique=True, nullable=True)
    microsoft_id = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    deadline = Column(DateTime, nullable=True)
    priority_score = Column(Float, default=0.0)
    estimated_study_time = Column(Float, default=0.0) # in hours
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    source = Column(String, index=True) # e.g., 'gmail', 'canvas', 'manual'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="tasks")
