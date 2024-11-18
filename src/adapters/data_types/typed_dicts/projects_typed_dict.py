from typing import TypedDict
from src import ProjectModel


class PaginatedProjectsTypedDict(TypedDict):
    projects: list[ProjectModel]
    total: int
    limit: int
    offset: int
