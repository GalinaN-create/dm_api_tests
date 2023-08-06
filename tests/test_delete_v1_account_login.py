import requests

from generic.helpers.dm_db import DmDatabase
from services.dm_api_account import Facade
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_delete_v1_account_login():
    api = Facade(host="http://localhost:5051")

    login = "admin957"
    email = "admin957@test.ru"
    password = "admin957"

    db = DmDatabase(user='postgres', password='admin', host='localhost', database='dm3.5')

    db.delete_user_by_login(login=login)

    dataset = db.get_user_by_login(login=login)
    assert len(dataset) == 0

    api.mailhog.delete_all_messages()

    dataset = db.get_user_by_login(login=login)
    for row in dataset:
        assert row['Login'] == login, f'User {login} not registered'
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
    api.login.set_headers(headers=token)

    response = api.login.logout_user(headers=token)
    return response
