import json
import requests
import tqdm
from gigachat import GigaChat

from config import main_config


def get_main_body(item: dict) -> str:
    description = item["description"]
    skills = item["key_skills"] if len(item["key_skills"]) > 0 else None

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
