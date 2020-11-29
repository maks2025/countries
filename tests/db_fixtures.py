import os
import socket
import sys
import uuid
from time import sleep

import docker as libdocker
import pytest
from aiopg.sa import create_engine as aio_create_engine
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

test_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(test_path, ".."))

from db import meta  # noqa

client = libdocker.from_env()


@pytest.fixture(scope="session")
def session_id():
    return str(uuid.uuid4())


@pytest.fixture(scope="session")
def unused_port():
    def f():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]

    return f


@pytest.yield_fixture(scope="session")
def postgres(unused_port, session_id):
    client = libdocker.from_env()
    port = unused_port()
    container = client.containers.run(
        "postgres:13.1-alpine",
        name=f"test-postgres-{session_id}",
        ports={5432: port},
        environment={
            "POSTGRES_USER": "test",
            "POSTGRES_PASSWORD": "test",
            "POSTGRES_DB": "test",
        },
        detach=True,
    )
    engine = create_engine(f"postgresql://test:test@localhost:{port}/test")

    # wil wait database
    while True:
        try:
            meta.create_all(engine)
        except OperationalError:
            sleep(1)
            continue
        else:
            break

    yield port
    container.stop()
    container.remove()


@pytest.fixture
def engine(loop, postgres):
    port = postgres
    engine = aio_create_engine(
        database="test",
        user="test",
        password="test",
        host="localhost",
        port=port,
    )
    return loop.run_until_complete(engine)


@pytest.fixture
def conn(loop, engine):
    return loop.run_until_complete(engine.acquire())
