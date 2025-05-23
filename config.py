import os
from dotenv import load_dotenv

load_dotenv()


def __convert_str_to_bool(value: str) -> bool:

    return value.lower() == 'true'


LOGIN_URL = os.getenv('LOGIN_URL')
PROJECTS_URL = os.getenv('PROJECTS_URL')
VALID_USERNAME = os.getenv('VALID_USERNAME')
VALID_PASSWORD = os.getenv('VALID_PASSWORD')
INVALID_USERNAME = os.getenv('INVALID_USERNAME')
INVALID_PASSWORD = os.getenv('INVALID_PASSWORD')

# Флаг запуска браузера в headless-режиме (без графического интерфейса - True, с графическим интерфейсом - False)
HEADLESS = __convert_str_to_bool(os.getenv('HEADLESS', 'False'))