import json
import requests
import gspread

from app.get_data import load_full_vacancies
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


def send_negotiation(
    vacancy_id: str, resume_id: str, message: str, access_token: str
) -> None:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "HH-User-Agent": main_config.HH_User_Agent,
    }
    params = {
        "vacancy_id": vacancy_id,
        "resume_id": resume_id,
        "message": message,
    }
    requests.post(main_config.negotiations_URL, headers=headers, params=params)


def send_all_negotiations() -> None:
    all_vacancies = load_full_vacancies()
    resume_id = "####"
    access_token = get_hh_token()

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
    gc = gspread.service_account(filename=main_config.google_service_account_filename)
    sht = gc.open_by_url(main_config.google_sheet_url)
    sht.append_row(data)
    return {"status": "Ok"}
