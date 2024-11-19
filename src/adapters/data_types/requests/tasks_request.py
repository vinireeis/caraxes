from pydantic import BaseModel, field_validator, model_validator
from datetime import date
from src.domain.enums.tasks.enum import TaskStatusEnum, TaskPriorityEnum


class BaseTaskRequest(BaseModel):
    name: str
    description: str | None = None
    status: TaskStatusEnum
    priority: TaskPriorityEnum = TaskPriorityEnum.MEDIUM
    deadline: date | None = None

    @model_validator(mode="before")
    def check_unique_assigned_users(cls, values):
        assigned_users = values.get("assigned_users", [])
        values["assigned_users"] = list(set(assigned_users))
        return values

    @field_validator("deadline")
    def validate_deadline(cls, deadline: date | None) -> date | None:
        if deadline and deadline < date.today():
            raise ValueError("Deadline cannot be in the past")
        return deadline


class NewTaskRequest(BaseTaskRequest):
    assigned_users: list[int] = []
    pass


class UpdateTaskRequest(BaseTaskRequest):
    pass


class UpdateTaskStatusRequest(BaseModel):
    status: TaskStatusEnum
