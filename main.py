from pathlib import Path

import pytz
from aiohttp import web
from db import init_pg, close_pg
from dotenv import load_dotenv
from aiocron import crontab
from services import load
from views import reload, search_codes, codes_countries, info_about_country

env_path = Path(".") / "example.env"
load_dotenv(dotenv_path=env_path)


@crontab("0 2 * * *", tz=pytz.timezone("Europe/Moscow"))
async def periodic():
    """
    Periodic start update data - 02:00 MSK
    :return:
    """
    await load(app)


app = web.Application()
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)

app.add_routes(
    [
        web.post("/reload", reload),
        web.post("/search_codes", search_codes),
        web.get("/codes_countries", codes_countries),
        web.get("/info_about_country", info_about_country),
    ]
)


if __name__ == "__main__":
    web.run_app(app)
