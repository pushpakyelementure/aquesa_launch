import os
import pytest
from httpx import AsyncClient

from starlette.testclient import TestClient

from app import main
from app.db import config
from app.auth.config import firebase_init

from app.config import get_settings, Settings


def get_settings_override():
    return Settings(
        environment="testing",
        testing=True,
        db_uri=os.environ.get("AQUESA_DB_DEV_TEST_URI"),
        db_name=os.environ.get("AQUESA_TEST_DB_NAME"),
    )


@pytest.fixture(scope="module")
def test_app():
    main.app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(main.app) as test_client:

        yield test_client


@pytest.fixture
async def test_app_with_db():
    # set up
    app = main.app
    app.dependency_overrides[get_settings] = get_settings_override
    await firebase_init()
    await config.init_db(
        os.environ.get("AQUESA_DB_DEV_TEST_URI"),
        os.environ.get("AQUESA_TEST_DB_NAME"),
    )

    # testing
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    # tear down
