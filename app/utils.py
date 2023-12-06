import json

import requests
import gspread
from gspread import Client, Spreadsheet, Worksheet

from app.get_data import load_full_vacancies, get_vacancy_description_by_id
from app.processing_data import get_data_for_table
from config import main_config


def get_hh_token() -> str:
    params = {
        "grant_type": "authorization_code",
        "client_id": main_config.client_id,
        "client_secret": main_config.client_secret,
        "code": main_config.code,
    }
    response = requests.post(main_config.token_URL, data=params)
    access_token = response.json()["access_token"]

    return access_token


def get_id_resume(access_token: str) -> None:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "HH-User-Agent": main_config.HH_User_Agent,
    }
    response = requests.get("https://api.hh.ru/resumes/mine", headers=headers)
    resume_list = response.json()["items"]

    print(resume_list)


def send_negotiation(vacancy_id: str) -> None:
    vacancy_description = get_vacancy_description_by_id(vacancy_id)
    message = vacancy_description["cover_letter"]

    headers = {
        "Authorization": f"Bearer {main_config.hh_token}",
        "HH-User-Agent": main_config.HH_User_Agent,
    }
    params = {
        "vacancy_id": vacancy_id,
        "resume_id": main_config.hh_resume_id,
        "message": message,
    }

    requests.post(main_config.negotiations_URL, headers=headers, params=params)

    data = get_data_for_table(vacancy_id)
    add_row_to_goggle_sheet(data)


def send_all_negotiations() -> None:
    all_vacancies = load_full_vacancies()
    resume_id = main_config.hh_resume_id
    access_token = main_config.hh_token

    for vacancy in all_vacancies:
        send_negotiation(
            vacancy_id=vacancy["id"],
            resume_id=resume_id,
            message=vacancy["cover_letter"],
            access_token=access_token,
        )


def get_all_negotiations() -> json:
    params = {"status": "active"}
    hh_token = get_hh_token()
    headers = {
        "Authorization": f"Bearer {hh_token}",
        "HH-User-Agent": main_config.HH_User_Agent,
    }
    response_data = requests.get(
        url=main_config.negotiations_URL, headers=headers, params=params
    )
    if not response_data.ok:
        print("Ошибка: ", response_data)
        return {}
    all_negotiations = response_data.json()["items"]
    return all_negotiations


def add_row_to_goggle_sheet(data: list[str]) -> dict:
    sa: Client = gspread.service_account(
        filename=main_config.google_service_account_filename
    )
    sh: Spreadsheet = sa.open_by_key("1NN0jWjesc3jKnZ6IWq0yLS73Jxi3mgtr0LDIx9ELs1s")
    wks: Worksheet = sh.worksheet("Активный поиск")

    wks.append_row(data)

    return {"status": "Ok"}
