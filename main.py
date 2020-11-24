from aiohttp import web

from db import init_pg, close_pg
from views import reload, search_codes, codes_countries, code_country

app = web.Application()
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)

app.add_routes([
    web.post('/reload', reload),
    web.post('/search_codes', search_codes),
    web.get('/codes_countries', codes_countries),
    web.get('/code_country', code_country),
])


if __name__ == '__main__':
    web.run_app(app)
