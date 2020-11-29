import pytest
from aiohttp import ClientSession
from sqlalchemy import select

from db import country
from services import request_data, load


@pytest.mark.vcr
async def test_request_names():
    async with ClientSession() as session:
        response = await request_data(session, "http://country.io/names.json")
        assert response.status == 200


@pytest.mark.vcr
async def test_request_phone_codes():
    async with ClientSession() as session:
        response = await request_data(session, "http://country.io/phone.json")
        assert response.status == 200


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_load(conn):
    await load(conn)
    s = select([country.c.code, country.c.name, country.c.phone_code])
    r = await conn.execute(s)
    assert r is not None
    s = s.where(country.c.code == "RU")
    r = await conn.execute(s)
    assert await r.fetchone() == ("RU", "Russia", "7")
