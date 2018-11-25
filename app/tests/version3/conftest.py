import os
import pytest

from flask_jwt_extended import create_access_token

from app import create_app
from app.db_config import create_tables, destroy_tables



@pytest.yield_fixture(scope="session")
def app():
    app = create_app('testing')
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture(scope="module")
def init_db(app):
    with app.app_context():
        create_tables()
        print("created tables")
        yield
        destroy_tables('parcels')
        print("dropped tables")


@pytest.fixture(scope="function")
def client(app):
    yield app.test_client()


@pytest.fixture(scope="function")
def token(app):
    def func():
        token = create_access_token(1)
        auth = {
            "Authorization": "bearer %s" % token
        }
        return auth
    return func
