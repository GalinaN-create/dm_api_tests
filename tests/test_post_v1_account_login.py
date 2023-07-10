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
    json = {
        "login": "admin8",
        "password": "admin8@test.ru",
        "rememberMe": False
    }
    response = api.account.post_v1_account(
        json=json
    )
    print(response)