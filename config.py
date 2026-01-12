import os
import tempfile

class Config:
    """Base configuration."""
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 8025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None


class DevelopmentConfig(Config):
    """Development configuration."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    TESTING = False


class TestConfig(Config):
    """Testing configuration with file-based SQLite database for thread safety."""
    # Use a temporary file-based database instead of in-memory
    # This ensures all threads share the same database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TESTING = True
    # Disable CSRF during testing for easier form submission
    WTF_CSRF_ENABLED = False
