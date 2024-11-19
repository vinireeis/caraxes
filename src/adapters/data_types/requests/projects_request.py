from datetime import date
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator
from src.domain.enums.projects.enum import ProjectStatusEnum


class BaseProjectRequest(BaseModel):
    user_id: int
    name: str
    status: ProjectStatusEnum
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @model_validator(mode="before")
    def validate_dates(cls, values):
        start_date = values.get("start_date")
        end_date = values.get("end_date")

        if isinstance(start_date, str):
            start_date = date.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = date.fromisoformat(end_date)

        values["start_date"] = start_date
        values["end_date"] = end_date

        if start_date and end_date and end_date <= start_date:
            raise ValueError("end_date must be greater than start_date")

        if start_date and start_date < date.today():
            raise ValueError("Start date cannot be in the past")

        return values

    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        if len(name.strip()) < 3:
            raise ValueError("Project name must have at least 3 characters")
        return name.strip()


class NewProjectRequest(BaseProjectRequest):
    pass


class UpdateProjectRequest(BaseProjectRequest):
    pass
