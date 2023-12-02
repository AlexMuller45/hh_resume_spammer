import os
from flask import Config

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(Config):
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or "A SECRET KEY"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    CSRF_ENABLED: bool = True
    DEBUG: bool = False
    VACANCIES_URL: str = os.environ.get("VACANCIES_URL")
    DICTIONARIES_URL: str = os.environ.get("DICTIONARIES_URL")
    vacancies_filename: str = os.environ.get("VACANCIES_FILENAME")
    full_vacancies_filename: str = os.environ.get("FULL_VACANCIES_FILENAME")
    main_menu = [
        {"name": "Новый поиск", "url": "/"},
        {"name": "Список вакансий", "url": "/vacancies"},
        {"name": "Сопроводительные письма", "url": "/cover_letters"},
    ]


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    DEBUG = False


main_config = BaseConfig
