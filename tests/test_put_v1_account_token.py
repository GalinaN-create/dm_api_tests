import requests
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi

import time
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_token():
    mailhog = MailhogApi(host="http://localhost:5025")
    api = DmApiAccount(host="http://localhost:5051")
    json = {
        "login": "admin23",
        "email": "admin23@test.ru",
        "password": "admin23"
    }
    response = api.account.post_v1_account(
        json=json
    )
    assert response.status_code == 201, f'Статус код ответа должен быть равен 201, но он равен {response.status_code}'


    time.sleep(4)
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)

