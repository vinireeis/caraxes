from fastapi import FastAPI

from decouple import config

from src.externals.routers.projects.router import ProjectsRouter
from src.externals.routers.users.router import UsersRouter


class ApiInfrastructure:
    __root_path: str = config("ROOT_PATH")
    __app: FastAPI = None

    @classmethod
    def get_app(cls):
        if cls.__app is None:
            cls.__app = FastAPI(
                title="Caraxes API",
                description="Projects and tasks management",
                docs_url=f"{cls.__root_path}/docs",
                openapi_url=f"{cls.__root_path}/openapi.json",
            )
        cls.register_routers(app=cls.__app)
        return cls.__app

    @classmethod
    def register_routers(cls, app: FastAPI):
        cls.__include_users_router(app=app)
        cls.__include_projects_router(app=app)

    @staticmethod
    def __include_users_router(app: FastAPI):
        router = UsersRouter.get_users_router()
        app.include_router(router)

    @staticmethod
    def __include_projects_router(app: FastAPI):
        router = ProjectsRouter.get_projects_router()
        app.include_router(router)
