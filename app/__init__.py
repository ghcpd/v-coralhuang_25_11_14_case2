from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()


def create_app(config_class):
    """
    Application factory function.
    
    Args:
        config_class: Configuration class to use (DevelopmentConfig, TestConfig, etc.)
    
    Returns:
        Initialized Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)

    return app
