import copy
import os
import pytest
import sys

test_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(test_path, ".."))

from main import app


@pytest.yield_fixture(scope="function")
def cli(loop, aiohttp_client, engine):
    app_cp = copy.deepcopy(app)
    app_cp.on_startup.clear()
    app_cp.on_cleanup.clear()
    app_cp["db"] = engine
    return loop.run_until_complete(aiohttp_client(app_cp))
