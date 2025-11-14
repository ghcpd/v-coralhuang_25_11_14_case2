# app/__init__.py (fixed)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

try:
    from flask_login import LoginManager
except Exception:
    LoginManager = None

try:
    from flask_mail import Mail
except Exception:
    Mail = None

# extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager() if LoginManager else None
mail = Mail() if Mail else None


def create_app(config_class):
    app = Flask(__name__)
    # support either module or class passed
    if isinstance(config_class, type):
        app.config.from_object(config_class)
    else:
        app.config.from_mapping(config_class)

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    if login:
        login.init_app(app)
    mail.init_app(app)

    # import models so migrations know about them and to register models on the metadata
    from app import models
    with app.app_context():
        try:
            # optional CLI or init code may be placed here
            # if there is a "cli" module, register commands
            from app import cli
            cli.register_commands(app)
        except Exception:
            # not required; ignore missing or broken cli in tests
            pass

    return app
