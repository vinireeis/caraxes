from fastapi import FastAPI

from decouple import config

from src.externals.routers.clients.router import ClientsRouter


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
        cls.__include_clients_router(app=app)

    @staticmethod
    def __include_clients_router(app: FastAPI):
        router = ClientsRouter.get_clients_router()
        app.include_router(router)
