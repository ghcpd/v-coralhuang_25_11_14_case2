import os

basedir = os.path.abspath(os.path.dirname(__file__))

class TestConfig:
    TESTING = True
    DEBUG = False
    SECRET_KEY = 'test-secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_SUPPRESS_SEND = True  # suppress real sending in tests
    MAIL_USE_THREADING = False  # run synchronously in tests to avoid races
