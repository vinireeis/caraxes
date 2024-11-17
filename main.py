import uvicorn
from decouple import config
from pyfiglet import print_figlet

from src.externals.infrastructures.api.infrastructure import ApiInfrastructure

app = ApiInfrastructure.get_app()


if __name__ == "__main__":
    print(
        f"Server is ready at URL {config("HOST")}:{str(config("PORT")) + config("ROOT_PATH")}"
    )
    print_figlet(text="caraxes-api", colors="0;78;225", width=200)
    uvicorn.run(app, host="0.0.0.0", port=9000)
