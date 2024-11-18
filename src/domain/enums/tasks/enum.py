from enum import StrEnum


class ProjectStatus(StrEnum):
    PLANNING = "PLANNING"
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
