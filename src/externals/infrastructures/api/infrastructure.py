from fastapi import FastAPI

from decouple import config

from src.externals.infrastructures.api.middleware import Middleware
from src.externals.routers.projects.router import ProjectsRouter
from src.externals.routers.tasks.router import TasksRouter
from src.externals.routers.users.router import UsersRouter


class ApiInfrastructure:
    __root_path: str = config("ROOT_PATH")
    app: FastAPI = None

    @classmethod
    def get_app(cls):
        if cls.app is None:
            cls.app = FastAPI(
                title="Caraxes API",
                description="Projects and tasks management",
                docs_url=f"{cls.__root_path}/docs",
                openapi_url=f"{cls.__root_path}/openapi.json",
            )
        cls.register_routers(app=cls.app)
        cls.register_middlewares(app=cls.app)

        return cls.app

    @classmethod
    def register_middlewares(cls, app: FastAPI):
        Middleware.register_middleware(app)

    @classmethod
    def register_routers(cls, app: FastAPI):
        cls.__include_users_router(app=app)
        cls.__include_projects_router(app=app)
        cls.__include_tasks_router(app=app)

    @staticmethod
    def __include_users_router(app: FastAPI):
        router = UsersRouter.get_users_router()
        app.include_router(router)

    @staticmethod
    def __include_projects_router(app: FastAPI):
        router = ProjectsRouter.get_projects_router()
        app.include_router(router)

    @staticmethod
    def __include_tasks_router(app: FastAPI):
        router = TasksRouter.get_tasks_router()
        app.include_router(router)
