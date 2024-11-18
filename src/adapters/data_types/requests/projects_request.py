from datetime import datetime, UTC
from typing import Optional
from pydantic import BaseModel, field_validator, ValidationError
from src.domain.enums.projects.enum import ProjectStatusEnum


class BaseProjectRequest(BaseModel):
    user_id: int
    name: str
    status: ProjectStatusEnum
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    @field_validator("end_date")
    def validate_end_date(cls, end_date, values):
        start_date = values.get("start_date")
        if end_date and start_date and end_date <= start_date:
            raise ValidationError("end_date must be greater than start_date")
        return end_date

    @field_validator("start_date")
    def validate_start_date(cls, start_date: datetime | None) -> datetime | None:
        if start_date and start_date < datetime.now(UTC):
            raise ValidationError("Start date cannot be in the past")
        return start_date

    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        if len(name.strip()) < 3:
            raise ValidationError("Project name must have at least 3 characters")
        return name.strip()


class NewProjectRequest(BaseProjectRequest):
    pass


class UpdateProjectRequest(BaseProjectRequest):
    pass
