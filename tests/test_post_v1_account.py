import time

from generic.helpers.dm_db import DmDatabase
from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade
from generic.helpers.mailhog import MailhogApi
import structlog
from dm_api_account.models.registration_model import Registration
from hamcrest import assert_that, has_properties, starts_with, instance_of, all_of, has_entries
from dm_api_account.models.user_envelope import UserRole
import generic

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


# TODO готов
def test_post_v1_account():
    api = Facade(host="http://localhost:5051")

    login = "admin1"
    email = "admin1@test.ru"
    password = "admin1"
    orm = OrmDatabase(user='postgres', password='admin', host='localhost', database='dm3.5')

    orm.delete_user_by_login(login=login)

    dataset = orm.get_user_by_login(login=login)
    assert len(dataset) == 0

    api.mailhog.delete_all_messages()

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Login == login, f'User {login} not registered'

    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Login == login, f'User {login} registered'
        assert row['Activated'] is False, f'User {login} was not activated'

    # api.account.activate_registered_user(login=login)

    orm.activated_new_user(login=login)

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Activated is True, f'User {login} not activated'

    response = api.login.login_user(
        login=login,
        password=password
    )

    assert_that(response.json()['resource'], has_entries(
        {
            "login": "admin1",
            "roles": ["Guest", "Player"],
            "rating": ({
                "enabled": True,
                "quality": 0,
                "quantity": 0
            })

        }
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
