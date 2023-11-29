import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "A SECRET KEY"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    DEBUG = False
