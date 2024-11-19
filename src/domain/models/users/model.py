from datetime import datetime, UTC
from typing import List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models.orm_base.model import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    role: Mapped[Optional[str]] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(), onupdate=datetime.now()
    )

    projects: Mapped[List["ProjectModel"]] = relationship(back_populates="user")
    tasks: Mapped[List["TaskModel"]] = relationship(
        secondary="task_assignments", back_populates="assigned_users"
    )
