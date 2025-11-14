"""Application factory and extension wiring."""

from __future__ import annotations

from typing import Any

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
mail = Mail()


def create_app(config_object: Any | None = None) -> Flask:
    """Create and configure the Flask application."""
    from config import Config

    app = Flask(__name__)
    if config_object is None:
        config_object = Config

    if isinstance(config_object, dict):
        app.config.from_mapping(config_object)
    else:
        app.config.from_object(config_object)

    db.init_app(app)
    mail.init_app(app)

    # Register models so metadata is ready for migrations/tests.
    with app.app_context():
        from app import models  # noqa: F401

    return app
