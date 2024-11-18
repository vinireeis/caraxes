from enum import StrEnum


class ProjectStatus(StrEnum):
    PLANNING = "PLANNING"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
