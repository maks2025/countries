import json

from aiohttp import web

from db import (get_all, get_codes_countries_by_search_string, get_codes_of_countries,
                get_country_info_by_code)
from services import load


async def reload(request):
    """
    Reload data from country.io
    :param request:
    :return:
    """
    await load(request.app)

    async with request.app['db'].acquire() as conn:
        data = await get_all(conn)

    return web.Response(text=json.dumps(data))


async def search_codes(request):
    """
    Returned countries codes for countries matched with search string
    :param request:
    :return:
    """
    data = await request.json()
    search_string = data.get('search_string')

    async with request.app['db'].acquire() as conn:
        data = await get_codes_countries_by_search_string(conn, search_string)
    return web.Response(text=json.dumps(data))


async def codes_countries(request):
    """
    Returned list codes countries matched with search string
    :param request:
    :return:
    """
    async with request.app['db'].acquire() as conn:
        data = await get_codes_of_countries(conn)
    return web.Response(text=json.dumps(data))


async def code_country(request):
    query = dict(request.rel_url.query)
    code = query.get('code')
    async with request.app['db'].acquire() as conn:
        data = await get_country_info_by_code(conn, code)
    return web.Response(text=json.dumps(data))
