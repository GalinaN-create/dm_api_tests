import time

import requests
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_login():
    api = DmApiAccount(host="http://localhost:5051")
    mailhog = MailhogApi(host='http://localhost:5025')
    json = {
        "login": "admin31",
        "email": "admin31@test.ru",
        "password": "admin31"
    }
    response = api.account.post_v1_account(json=json)
    assert response.status_code == 201, f'статус код создания аккаунта должен быть равен 201, а равен {response.status_code}'

    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
    assert response.status_code == 200, f'статус код получения токена не равен 200, а равен {response.status_code}'

    response = api.login.post_v1_account_login(json=json)
    assert response.status_code == 200, f"статус код входа в аккаунт должен быть 200, а равен {response.status_code}"

    print(response)
