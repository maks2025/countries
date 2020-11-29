from aiohttp import ClientSession

from db import update_or_create


async def request_data(session, url):
    return await session.get(url)


async def load(conn):
    async with ClientSession() as session:
        response = await request_data(session, "http://country.io/names.json")
        countries_data = await response.json()
        response = await request_data(session, "http://country.io/phone.json")
        phones_codes_data = await response.json()

        await update_or_create(conn, countries_data, kind="countries")
        await update_or_create(conn, phones_codes_data, kind="phone_codes")
