import time

import requests
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog
from dm_api_account.models.registration_model import RegistrationModel

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account():
    mailhog = MailhogApi(host="http://localhost:5025")
    api = DmApiAccount(host="http://localhost:5051")
    json = RegistrationModel(
        login="admin276",
        email="admin276@test.ru",
        password="admin276"
    )
    response = api.account.post_v1_account(json=json)
    assert response.status_code == 201, f'Статус код ответа должен быть равен 201, но он равен {response.status_code}'

    time.sleep(4)

    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
    print(response)
#
#
# def check_input_json(json):
#     for key, value in json.items():
#         if key == 'login':
#             assert isinstance(value, str), f'Тип значения в ключе {key} должен быть str, но получен {type(value)}'
#         if key == 'email':
#             assert isinstance(value, str), f'Тип значения в ключе {key} должен быть str, но получен {type(value)}'
#         if key == 'password':
#             assert isinstance(value, str), f'Тип значения в ключе {key} должен быть равен str, но получен {type(value)}'
