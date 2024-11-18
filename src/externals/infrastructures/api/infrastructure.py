from fastapi import FastAPI

from decouple import config

from src.externals.routers.users.router import UsersRouter


class ApiInfrastructure:
    __root_path = config("ROOT_PATH")

    @classmethod
    def get_app(cls):
        app = FastAPI(
            title="Caraxes API",
            description="Projects and tasks management",
            docs_url=cls.__root_path + "/docs",
            openapi_url=cls.__root_path + "/openapi.json",
        )

        cls.__register_routers()

        return app

    @classmethod
    def __register_routers(cls):
        app = cls.get_app()
        cls.__include_users_router(app=app)

    @staticmethod
    def __include_users_router(app: FastAPI):
        router = UsersRouter.get_users_router()
        app.include_router(router)
