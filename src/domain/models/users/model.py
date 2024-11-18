from datetime import datetime
from typing import List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models.orm_base.model import Base
from src.domain.models.projects.model import ProjectModel
from src.domain.models.tasks.model import TaskModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    role: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    projects: Mapped[List["ProjectModel"]] = relationship(back_populates="user")
    tasks: Mapped[List["TaskModel"]] = relationship(
        secondary="task_assignments", back_populates="assigned_users"
    )
