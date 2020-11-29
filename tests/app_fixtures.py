import os
import pytest
import sys

test_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(test_path, ".."))

from main import app


@pytest.fixture
def cli(loop, aiohttp_client, engine):
    app.on_startup.clear()
    app.on_cleanup.clear()
    app['db'] = engine
    return loop.run_until_complete(aiohttp_client(app))