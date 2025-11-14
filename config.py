import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_DEFAULT_SENDER = 'noreply@example.com'

class TestConfig(Config):
    TESTING = True
    # Use a file-based SQLite DB to allow multithread access
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    MAIL_SUPPRESS_SEND = False
    MAIL_BACKEND = 'console'
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    # Use a short timeout for tests
    EMAIL_SEND_ASYNC = False  # In tests run synchronously by default (deterministic)
