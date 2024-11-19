from datetime import datetime, date
from typing import List, Optional

from sqlalchemy import ForeignKey, String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.enums.tasks.enum import TaskStatusEnum, TaskPriorityEnum
from src.domain.models.orm_base.model import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Enum(TaskStatusEnum))
    priority: Mapped[str] = mapped_column(
        Enum(TaskPriorityEnum), default=TaskPriorityEnum.MEDIUM
    )
    deadline: Mapped[Optional[date]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(), onupdate=datetime.now()
    )

    project: Mapped["ProjectModel"] = relationship(back_populates="tasks")
    assigned_users: Mapped[List["UserModel"]] = relationship(
        secondary="task_assignments", back_populates="tasks", cascade="all, delete"
    )


class TaskAssignmentModel(Base):
    __tablename__ = "task_assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assigned_at: Mapped[datetime] = mapped_column(default=datetime.now())
