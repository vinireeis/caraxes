from datetime import UTC, datetime
from typing import Optional, List

from sqlalchemy import ForeignKey, String, Text, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.domain.enums.projects.enum import ProjectStatusEnum
from src.domain.models.orm_base.model import Base


class ProjectModel(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[ProjectStatusEnum] = mapped_column(Enum(ProjectStatusEnum))
    start_date: Mapped[Optional[datetime]] = mapped_column(default=datetime.now(UTC))
    end_date: Mapped[Optional[datetime]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )

    user: Mapped["UserModel"] = relationship(back_populates="projects")
    tasks: Mapped[List["TaskModel"]] = relationship(back_populates="project")
