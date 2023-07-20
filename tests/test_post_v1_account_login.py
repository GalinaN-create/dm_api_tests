import time

import requests
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog
from dm_api_account.models.registration_model import Registration
from dm_api_account.models.login_credentials_model import LoginCredentials
from hamcrest import assert_that, has_properties, has_entries
from dm_api_account.models.user_envelope import UserRole

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


# TODO Готово
def test_post_v1_account_login():
    api = DmApiAccount(host="http://localhost:5051")
    mailhog = MailhogApi(host='http://localhost:5025')
    json = Registration(
        login="admin401",
        email="admin401@test.ru",
        password="admin401"
    )
    json2 = LoginCredentials(
        login="admin401",
        password="admin401",
        rememberMe=True
    )

    response = api.account.post_v1_account(json=json)

    time.sleep(2)

    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
    assert_that(response.resource, has_properties(
        {
            "login": "admin401",
            "roles": [UserRole.guest, UserRole.player]

        }
    ))

    response = api.login.post_v1_account_login(json=json2)

    assert_that(response.json(), has_entries(
        {
            "resource": has_entries({"login": "admin401",
                                     "roles": ['Guest', 'Player']}),
            "metadata": has_entries({"email": "ad..0@te..u"})
        }
    ))

    print(response)
