from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, ValidationError


class BaseUserRequest(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = None

    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        name = name.strip()
        if len(name) < 2:
            raise ValidationError("Name must have at least 2 characters")
        return name


class NewUserRequest(BaseUserRequest):
    pass


class UpdateUserRequest(BaseUserRequest):
    pass
