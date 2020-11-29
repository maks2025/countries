import pytest

pytest_plugins = ["aiohttp.pytest_plugin", "db_fixtures"]


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")
    config.addinivalue_line("markers", "other: mark test as slow to run")


@pytest.fixture(scope="session")
def vcr_config():
    return {
        "record_mode": "once",
    }
