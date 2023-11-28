import json
import time

import requests
import tqdm


VACANCIES_URL: str = "https://api.hh.ru/vacancies"


def json_to_file(data: json, filename) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_vacancies(
    # название вакансии
    text: str = "python",
    # опыт работы ["noExperience", "between1And3"]
    experience: str | None = None,
    # тип занятости ["full", "part", "project", "probation"]
    employment: str | None = None,
    # график работы ["fullDay", "flexible", "remote"]
    schedule: str | None = "remote",
) -> json:
    params = {
        "per_page": 100,
        "page": 0,
        "period": 14,
        "text": text,
        "experience": experience,
        "employment": employment,
        "schedule": schedule,
    }

    response_data = requests.get(url=VACANCIES_URL, params=params)
    if not response_data.ok:
        print("Ошибка: ", response_data)
        return {}

    vacancies = response_data.json()["items"]
    pages = response_data.json()["pages"]

    for page in tqdm.trange(1, pages):
        params["page"] = page
        response_data = requests.get(url=VACANCIES_URL, params=params)
        if response_data.ok:
            response_json = response_data.json()
            vacancies.extend(response_json["items"])
        else:
            print(f"Ошибка на странице {page}: ", response_data)

    json_to_file(vacancies, vacancies.json)
    return vacancies


def get_full_description(vacancies: json) -> json:
    vacancies_full: list[dict] = []
    for entry in tqdm.tqdm(vacancies):
        vacancy_id = entry["id"]
        description = requests.get(f"{VACANCIES_URL}/{vacancy_id}")
        vacancies_full.append(description.json())
        time.sleep(0.2)

    json_to_file(vacancies_full, "vacancies_full.json")
    return vacancies_full
