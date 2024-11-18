from datetime import datetime, UTC
from typing import List, Optional

from sqlalchemy import ForeignKey, String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.enums.tasks.enum import TaskStatus, TaskPriority
from src.domain.models.orm_base.model import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Enum(TaskStatus))
    priority: Mapped[str] = mapped_column(
        Enum(TaskPriority), default=TaskPriority.MEDIUM
    )
    deadline: Mapped[Optional[datetime]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )

    project: Mapped["ProjectModel"] = relationship(back_populates="tasks")
    assigned_users: Mapped[List["UserModel"]] = relationship(
        secondary="task_assignments", back_populates="tasks"
    )


class TaskAssignmentModel(Base):
    __tablename__ = "task_assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assigned_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
