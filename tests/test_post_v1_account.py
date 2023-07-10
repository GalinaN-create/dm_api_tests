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


def test_post_v1_account():
    mailhog = MailhogApi(host="http://localhost:5025")
    api = DmApiAccount(host="http://localhost:5051")
    json = {
        "login": "admin22",
        "email": "admin22@test.ru",
        "password": "admin22"
    }
    time.sleep(4)
    response = api.account.post_v1_account(
        json=json
    )
    assert response.status_code == 201, f'Статус код ответа должен быть равен 201, но он равен {response.status_code}'

    time.sleep(4)
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
