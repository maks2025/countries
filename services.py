from aiohttp import ClientSession

from db import update_or_create


async def load(app):
    async with ClientSession() as session:
        async with session.get('http://country.io/names.json') as response:
            countries_data = await response.json()
        async with session.get('http://country.io/phone.json') as response:
            phones_codes_data = await response.json()

    async with app['db'].acquire() as conn:
        await update_or_create(conn, countries_data, kind='countries')
        await update_or_create(conn, phones_codes_data, kind='phone_codes')
