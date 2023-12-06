
import os
from pprint import pprint
from dotenv import load_dotenv

import requests

from config import main_config

load_dotenv()
token = hh_token = os.environ.get(
    "HH_TOKEN"
)

headers = {
    "Authorization": f"Bearer {token}",
    "HH-User-Agent": main_config.HH_User_Agent,
}

response = requests.get("https://api.hh.ru/resumes/mine", headers=headers)
resumes_list = response.json()

for item in resumes_list["items"]:
    print(f"ID резюме: [ {item["id"]} ] # должность [ {item["title"]} ]")
