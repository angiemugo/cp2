import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    test_db_path = os.path.join(os.path.dirname(__file__), 'tests/testdb.sqlite')
    db_uri = 'sqlite:///{}'.format(test_db_path)
    TESTING = True
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False


config = {
    "production": ProductionConfig,
    "staging": StagingConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": Config,
}
