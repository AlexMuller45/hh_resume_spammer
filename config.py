import os
from flask import Config

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(Config):
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or "A SECRET KEY"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    CSRF_ENABLED: bool = True
    DEBUG: bool = False
    VACANCIES_URL: str = os.environ.get("HH_VACANCIES_URL")
    DICTIONARIES_URL: str = os.environ.get("HH_DICTIONARIES_URL")
    negotiations_URL: str = os.environ.get("HH_NEGOTIATIONS_URL")
    vacancies_filename: str = os.environ.get("VACANCIES_FILENAME")
    full_vacancies_filename: str = os.environ.get("FULL_VACANCIES_FILENAME")

    main_menu = [
        {"name": "Новый поиск", "url": "/"},
        {"name": "Список вакансий", "url": "/vacancies"},
        {"name": "Сопроводительные письма", "url": "/cover_letters"},
        {"name": "Активные отклики", "url": "/vacancies/negotiations"},
    ]

    giga_token: str = os.environ.get("GIGA_TOKEN")

    vac_exception: str = os.environ.get("vac_exception")
    vac_default: str = os.environ.get("vac_default")
    my_skills: str = os.environ.get("my_skills")

    hh_resume_id = os.environ.get("RESUME_ID")
    hh_client_id = os.environ.get("HH_CLIENT_ID")
    hh_client_secret = os.environ.get("HH_CLIENT_SECRET")
    hh_token = os.environ.get("HH_TOKEN")

    hh_token_URL = os.environ.get("HH_TOKEN_URL")
    HH_User_Agent = os.environ.get("HH_User_Agent")
    google_service_account_filename = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILENAME")
    google_sheet_url = os.environ.get("GOOGLE_SHEET_URL")
    google_sheet_key = os.environ.get("GOOGLE_SHEET_KEY ")

    my_name = os.environ.get("MY_NAME")
    my_phone = os.environ.get("MY_PHONE")
    my_contact = os.environ.get("MY_CONTACT")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    DEBUG = False


main_config = BaseConfig
