from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    # If app has a CLI module that needs registration, the module should accept the app
    try:
        from app import cli
        if hasattr(cli, 'register_commands'):
            cli.register_commands(app)
    except Exception:
        # ignore if not present (simple app)
        pass

    return app
