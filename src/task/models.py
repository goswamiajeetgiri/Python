from sqlalchemy import Column, Integer, String, Boolean
from src.utils.db import Base

class TaskModel(Base):
    __tablename__ = "user_tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(500))
    is_completed = Column(Boolean, default=False)
