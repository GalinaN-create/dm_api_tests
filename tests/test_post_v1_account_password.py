import requests

from generic.helpers.dm_db import DmDatabase
from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade
from hamcrest import assert_that, all_of, has_properties, not_, empty, instance_of, has_entries
from dm_api_account.models.user_envelope import UserRole
import structlog
from dm_api_account.models.reset_password_model import ResetPassword

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


# TODO готов
def test_post_v1_account_password():
    api = Facade(host="http://localhost:5051")

    login = "admin803"
    email = "admin803@test.ru"
    password = "admin803"

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

    api.account.activate_registered_user(login=login)

    api.login.login_user(
        login=login,
        password=password
    )
    token = api.login.get_auth_token(login=login, password=password)

    api.account.set_headers(headers=token)
    response = api.account.reset_password(
        login=login,
        email=email
    )

    assert_that(response.json()['resource'], has_entries(
        {
            "login": "admin803",
            "roles": ["Guest", "Player"],
            "rating": ({
                "enabled": True,
                "quality": 0,
                "quantity": 0
            })

        }
    ))
    orm.db.close_connection()


