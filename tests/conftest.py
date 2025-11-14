"""Pytest fixtures for the Flask application."""

import pytest

from app import create_app, db
from config import TestConfig


@pytest.fixture
def app():
    """Provide a Flask app configured for testing and ensure clean DB state."""
    app = create_app(TestConfig)
    ctx = app.app_context()
    ctx.push()

    db.create_all()
    yield app

    db.session.remove()
    db.drop_all()
    ctx.pop()
