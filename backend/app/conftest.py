import pytest
from flask import Flask
from . import create_app, redis_store

def setup_function(function):
    redis_store.flushdb()


def teardown_function(function):
    redis_store.flushdb()

@pytest.fixture
def app(request):
    """Session-wide test `Flask` application."""
    # app = create_app('testing')
    app = create_app()
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture
def client(app):
    return app.test_client()

