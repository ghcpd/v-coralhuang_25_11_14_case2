import os
import sys

import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from config import TestConfig


@pytest.fixture(scope="function")
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def app_ctx(app):
    """Provide a pushed app context for tests that need it."""
    with app.app_context():
        yield app
