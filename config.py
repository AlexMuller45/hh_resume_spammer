import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or "A SECRET KEY"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    CSRF_ENABLED: bool = True
    DEBUG: bool = False
    VACANCIES_URL: str = os.environ.get("VACANCIES_URL")
    DICTIONARIES_URL: str = os.environ.get("DICTIONARIES_URL")
    vacancies_filename: str = os.environ.get("VACANCIES_FILENAME")
    vac_exception: str = (
        "NOT JAVA "
        "NOT JavaScript "
        "NOT TypeScript "
        "NOT 1C "
        "NOT аналитик "
        "NOT Frontend "
    )


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    DEBUG = False


main_config = BaseConfig
