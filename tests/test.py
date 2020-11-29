import pytest
from aiohttp import ClientSession, web
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
async def test_load(conn):
    await load(conn)
    s = select([country.c.code, country.c.name, country.c.phone_code])
    r = await conn.execute(s)
    assert r is not None
    s = s.where(country.c.code == 'RU')
    r = await conn.execute(s)
    assert await r.fetchone() == ('RU', 'Russia', '7')


async def test_search_codes(cli, loop):
    resp = await cli.post('/search_codes', json={'search_string': 'r'})
    assert resp.status == 201
    assert sorted(await resp.json()) == sorted(['RU', 'RW', 'RE', 'RO', 'CG'])


async def test_info_about_country(cli):
    resp = await cli.get('/info_about_country', params={'code': 'SV'})
    assert resp.status == 201
    info = await resp.json()
    assert sorted(info) == sorted(["SV", "El Salvador", "503"])


async def test_codes_countries(cli):
    resp = await cli.get('/codes_countries')
    assert resp.status == 201

