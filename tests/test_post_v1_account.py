import time

from services.dm_api_account import Facade
from generic.helpers.mailhog import MailhogApi
import structlog
from dm_api_account.models.registration_model import Registration
from hamcrest import assert_that, has_properties, starts_with, instance_of, all_of
from dm_api_account.models.user_envelope import UserRole
import generic
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


# TODO готов
def test_post_v1_account():
    mailhog = MailhogApi(host="http://localhost:5025")
    api = Facade(host="http://localhost:5051")
    # Register new user

    response = api.account.register_new_user(
        login="admin994",
        email="admin994@test.ru",
        password="admin994")
    print(response)
    time.sleep(4)

    # Activate token

    token = generic.helpers.account.activate_register_user()
    response = api.account.put_v1_account_token(token=token)

    print(response)

    # login user
    ...

    assert_that(response.resource, all_of(
        has_properties({
            "login": "admin994",
            "roles": [UserRole.guest, UserRole.player]
        }),
        has_properties(
            {"login": starts_with("admin994")
             }),
        has_properties({
            "rating": has_properties({
                "enabled": instance_of(bool)
            })
        })
    ))

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
