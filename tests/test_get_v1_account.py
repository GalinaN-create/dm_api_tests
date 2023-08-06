import requests

from generic.helpers.dm_db import DmDatabase
from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade
import structlog
from hamcrest import assert_that, has_properties
from dm_api_account.models.user_envelope import UserRole

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_get_v1_account():
    api = Facade(host="http://localhost:5051")
    login = "admin918"
    email = "admin918@test.ru"
    password = "admin918"

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

    api.account.activate_registered_user(
        login=login
    )

    api.login.login_user(
        login=login,
        password=password
    )

    token = api.login.get_auth_token(login=login, password=password)
    api.account.set_headers(headers=token)

    response = api.account.get_current_user_info()
    orm.db.close_connection()
    return response
