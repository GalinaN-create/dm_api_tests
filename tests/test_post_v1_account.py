import time

import requests
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog
from dm_api_account.models.registration_model import Registration
from hamcrest import assert_that, has_properties, starts_with, instance_of, all_of, contains
from dm_api_account.models.user_envelope import UserRole

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account():
    mailhog = MailhogApi(host="http://localhost:5025")
    api = DmApiAccount(host="http://localhost:5051")
    json = Registration(
        login="admin280",
        email="admin280@test.ru",
        password="admin280"
    )
    response = api.account.post_v1_account(json=json)
    time.sleep(4)

    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)

    assert_that(response.resource, all_of(
        has_properties({
            "login": "admin999",
            "roles": [UserRole.guest, UserRole.player]
        }),
        has_properties(
            {"login": starts_with("admin999")
             }),
        has_properties({
            "rating": has_properties({
                "enabled": instance_of(bool)
            })
        })
    ))

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
