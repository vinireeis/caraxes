from pydantic import BaseModel, field_validator
from datetime import datetime, UTC
from src.domain.enums.tasks.enum import TaskStatusEnum, TaskPriorityEnum


class BaseTaskRequest(BaseModel):
    name: str
    description: str | None = None
    status: TaskStatusEnum
    priority: TaskPriorityEnum = TaskPriorityEnum.MEDIUM
    deadline: datetime | None = None
    assigned_users: list[int] = []

    @field_validator("deadline")
    def validate_deadline(cls, deadline: datetime | None) -> datetime | None:
        if deadline and deadline < datetime.now(UTC):
            raise ValueError("Deadline cannot be in the past")
        return deadline


class NewTaskRequest(BaseTaskRequest):
    pass


class UpdateTaskRequest(BaseTaskRequest):
    pass


class UpdateTaskStatusRequest(BaseModel):
    status: TaskStatusEnum
