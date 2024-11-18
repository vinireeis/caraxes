import uvicorn
from decouple import config
from pyfiglet import print_figlet

from src.externals.infrastructures.api.infrastructure import ApiInfrastructure

app = ApiInfrastructure.get_app()


def main():
    host = config("HOST", default="0.0.0.0")
    port = config("PORT", default=8000, cast=int)
    root_path = config("ROOT_PATH", default="/")
    print(f"Server is ready at URL {host}:{port}{root_path}")
    print_figlet(text="caraxes-api", colors="0;78;225", width=200)
    uvicorn.run(app, host="0.0.0.0", port=9000)


if __name__ == "__main__":
    main()
