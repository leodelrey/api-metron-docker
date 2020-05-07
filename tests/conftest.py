"""
You can auto-discover and run all tests with this command:

    $ pytest

Documentation:

* https://docs.pytest.org/en/latest/
* https://docs.pytest.org/en/latest/fixture.html
* http://flask.pocoo.org/docs/latest/testing/
"""
import os
from dotenv import load_dotenv
import pytest
from src.app import create_app, create_db
from src.models import db as _db


@pytest.yield_fixture(scope='session')
def app():

    # Load the environment variable
    load_dotenv(override=True)
    db_url = os.getenv('DATABASE_TEST_URL')

    # Create database if doesn't exist
    create_db(db_url)

    # Create the application
    _app = create_app('testing')
    _app.config['SQLALCHEMY_DATABASE_URI'] = db_url

    # Push the context of the application
    ctx = _app.app_context()
    ctx.push()

    yield _app

    # Pop the context
    ctx.pop()


@pytest.fixture(scope='session')
def testapp(app):
    # Create a test client for the application
    return app.test_client()


@pytest.yield_fixture(scope='session')
def db(app):
    # Create the tables
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def session(db):
    # Create a session for the tests
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)

    db.session = session_

    yield session_

    # Close and rollback the database
    transaction.rollback()
    connection.close()
    session_.remove()
