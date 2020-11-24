import os
from datetime import datetime
from typing import List

import aiopg.sa
from aiopg.sa.connection import SAConnection
from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, TIMESTAMP,
    select, insert, update,
)

meta = MetaData()

country = Table(
    'country', meta,

    Column('id', Integer, primary_key=True),
    Column('created_at', TIMESTAMP, default=datetime.utcnow, nullable=False),
    Column('updated_at', TIMESTAMP, nullable=True),
    Column('code', String(2), nullable=False, unique=True),
    Column('name', String(127), nullable=True),
    Column('phone_code', String(16), nullable=True)
)


async def init_pg(app):
    engine = await aiopg.sa.create_engine(
        database=os.getenv('DB'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def update_or_create(conn: SAConnection, data: dict, kind: str = None) -> None:
    """
    Insert/update data from country name or phone codes api
    :param conn:
    :param data:
    :param kind:
    :return:
    """
    for code, value in data.items():
        if kind == 'countries':
            values = {
                'code': code,
                'name': value
            }
        elif kind == 'phone_codes':
            values = {
                'code': code,
                'phone_code': value
            }
        else:
            raise ValueError(f'db.insert_phone_codes - wrong kind insertion: {kind}')

        s = select([country]).where(country.c.code == code)
        r = await conn.execute(s)
        r = await r.fetchone()

        if r is None:
            operation = insert(country).values(
                **values
            )
        else:
            operation = update(country).where(
                country.c.code == code
            ).values(
                updated_at=datetime.utcnow(),
                **values
            )
        await conn.execute(operation)


async def get_all(conn: SAConnection) -> List[tuple]:
    """
    Returned all records
    :param conn:
    :return:
    """
    fields = [country.c.code, country.c.name, country.c.phone_code]
    s = select(fields)
    r = await conn.execute(s)
    proxy_rows = await r.fetchall()
    return [pr.as_tuple() for pr in proxy_rows]


async def get_codes_countries_by_search_string(conn: SAConnection, search_string: str) -> List[str]:
    """
    Returned country list for given search string
    :param conn:
    :param search_string:
    :return:
    """
    fields = [country.c.code]
    s = select(fields).where(country.c.name.ilike(f'{search_string}%'))
    r = await conn.execute(s)
    proxy_rows = await r.fetchall()
    return [pr.as_tuple()[0] for pr in proxy_rows]


async def get_codes_of_countries(conn: SAConnection) -> List[str]:
    """
    Returned codes of countries
    :param conn:
    :return:
    """
    fields = [country.c.code]
    s = select(fields)
    r = await conn.execute(s)
    proxy_rows = await r.fetchall()
    return [pr.as_tuple()[0] for pr in proxy_rows]


async def get_country_info_by_code(conn: SAConnection, code: str) -> tuple:
    """
    Returned info for country by given code
    :param conn:
    :param code:
    :return:
    """
    fields = [country.c.code, country.c.name, country.c.phone_code]
    s = select(fields).where(country.c.code == code)
    r = await conn.execute(s)
    r = await r.fetchone()
    return r.as_tuple()
