from datetime import datetime
import tqdm
from gigachat import GigaChat

from config import main_config
from app.get_data import (
    load_vacancies,
    load_full_vacancies,
    json_to_file,
    get_vacancy_description_by_id,
)


def check_matching_lists(vac_list: list[str]) -> tuple[int, list[str]]:
    my_skills_list = [
        skill.strip() for skill in main_config.my_skills.lower().split(",")
    ]
    intersection = set(vac_list) & set(my_skills_list)
    result = (len(intersection) / len(vac_list)) * 100
    return int(result), list(intersection)


def add_coincidence_in_vacancy(vac_id: str, value: int) -> None:
    vacancies = load_vacancies()
    for vac in vacancies:
        if vac["id"] == vac_id:
            vac["coincidence"] = value
    json_to_file(vacancies, filename=main_config.vacancies_filename)


def check_skills(data: list[dict]):
    for item in tqdm.tqdm(data):
        if item["key_skills"]:
            vacancy_skills_list = [elem["name"].lower() for elem in item["key_skills"]]
            coincidence, suitable_skills = check_matching_lists(vacancy_skills_list)
            item["coincidence"] = coincidence
            item["suitable_skills"] = suitable_skills
            add_coincidence_in_vacancy(item["id"], coincidence)
        else:
            item["coincidence"] = 1
            item["suitable_skills"] = ["python", "GigaChat"]
            add_coincidence_in_vacancy(item["id"], 1)

    json_to_file(data, filename="vacancies_full.json")


def get_main_body(item: dict) -> str:
    description = item["description"]

    promt = (
        f"Напиши краткое сопроводительное письмо на вакансию по описанию: {description}"
    )

    with GigaChat(
        credentials=main_config.giga_token,
        scope="GIGACHAT_API_PERS",
        verify_ssl_certs=False,
    ) as giga:
        response = giga.chat(promt)

    return response.choices[0].message.content


def generate_letter(item: dict) -> str:
    main_body = get_main_body(item)
    beginning_header = "Уважаемый"
    index_end_header = main_body.find(",")

    if beginning_header in main_body and index_end_header != -1:
        main_body = main_body[index_end_header + 1 :].strip()

    index_begin_footer = main_body.find("С уважением")
    beginning_footer = "С уважением,"

    if beginning_footer in main_body and index_begin_footer != -1:
        main_body = main_body[:index_begin_footer].strip()

    return (
        f"Здравствуйте!"
        f"\n{main_body}"
        f"\nС уважением,"
        f"\n{main_config.my_name}."
        f"\n{main_config.my_phone}, "
        f"\n{main_config.my_contact}."
    )


def generate_all_latter(all_vacancies: list[dict]) -> None:
    for vacancy in tqdm.tqdm(all_vacancies):
        cover_letter = generate_letter(vacancy)
        vacancy["cover_letter"] = cover_letter
    json_to_file(all_vacancies, filename=main_config.full_vacancies_filename)


def del_vacancy_by_id(vac_id: str) -> None:
    vacancies = load_vacancies()
    for vac in vacancies:
        if vac["id"] == vac_id:
            index = vacancies.index(vac)
            del vacancies[index]
            json_to_file(vacancies, filename=main_config.vacancies_filename)
            break

    full_vacancies = load_full_vacancies()
    for vac in full_vacancies:
        if vac["id"] == vac_id:
            index = full_vacancies.index(vac)
            del full_vacancies[index]
            json_to_file(full_vacancies, filename=main_config.full_vacancies_filename)
            break


def get_data_for_table(vac_id: str) -> list[str]:
    data = get_vacancy_description_by_id(vac_id)
    return [
        "NN",
        data["name"],
        data["employer"]["name"],
        data["alternate_url"],
        data["cover_letter"],
        datetime.today().strftime("%Y-%m-%d"),
        "",
        "hh.ru",
    ]
