from typing import TypedDict
from src import TaskModel


class PaginatedTasksTypedDict(TypedDict):
    tasks: list[TaskModel]
    total: int
    limit: int
    offset: int
