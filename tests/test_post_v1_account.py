import time

import requests
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi


def test_post_v1_account():
    mailhog = MailhogApi(host="http://localhost:5025")
    api = DmApiAccount(host="http://localhost:5051")
    json = {
        "login": "admin12",
        "email": "admin12@test.ru",
        "password": "admin1212"
    }
    response = api.account.post_v1_account(
        json=json
    )
    time.sleep(1)
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
    # print(response)
    print(response.json())
