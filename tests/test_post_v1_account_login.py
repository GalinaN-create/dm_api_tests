import time

import requests
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog
from dm_api_account.models.registration_model import Registration
from dm_api_account.models.login_credentials_model import LoginCredentials

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_login():
    api = DmApiAccount(host="http://localhost:5051")
    mailhog = MailhogApi(host='http://localhost:5025')
    json = Registration(
        login="admin306",
        email="admin306@test.ru",
        password="admin306"
    )
    json2 = LoginCredentials(
        login=json.login,
        password=json.password,
        rememberMe=True
    )

    response = api.account.post_v1_account(json=json)

    time.sleep(2)

    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)

    response = api.login.post_v1_account_login(json=json)

    print(response)
