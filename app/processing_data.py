import json
import requests
import tqdm
from gigachat import GigaChat

from config import main_config
from app.get_data import load_vacancies, load_full_vacancies, json_to_file


def check_matching_lists(vac_list: list[str]) -> tuple[int, list[str]]:
    my_skills_list = main_config.my_skills.lower().split(",")
    intersection = set(vac_list) & set(my_skills_list)
    result = (len(intersection) / len(vac_list)) * 100
    return int(result), list(intersection)


def add_coincidence_in_vacancy(vac_id: str, value: int) -> None:
    vacancies = load_vacancies()
    for vac in vacancies:
        if vac["id"] == vac_id:
            vac["coincidence"] = value
    json_to_file(vacancies, filename=main_config.vacancies_filename)


def check_skills():
    full_vacancies = load_full_vacancies()

    for item in tqdm.tqdm(full_vacancies):
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

    json_to_file(full_vacancies, filename="vacancies_full.json")


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
        print(response.choices[0].message.content)

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
        f"\nМельников Алексей."
        f"\n+7 (919) 561-67-71, "
        f"\nmas-chel@mail.ru, https://t.me/aleksey_melnikov_77"
    )


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
