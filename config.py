import os
from pathlib import Path


def _get_bool(name: str, default: bool = False) -> bool:
    """Parse truthy environment variables consistently."""
    return os.environ.get(name, str(default)).lower() in {"1", "true", "yes", "on"}


class Config:
    BASE_DIR = Path(__file__).parent
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'app.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 25))
    MAIL_USE_TLS = _get_bool("MAIL_USE_TLS", False)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@example.com")
    MAIL_SUPPRESS_SEND = _get_bool("MAIL_SUPPRESS_SEND", True)
    EMAIL_USE_ASYNC = _get_bool("EMAIL_USE_ASYNC", True)


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"check_same_thread": False}}
    MAIL_SUPPRESS_SEND = True
    EMAIL_USE_ASYNC = False
