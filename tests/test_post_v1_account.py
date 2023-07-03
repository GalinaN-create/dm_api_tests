import requests
from services.dm_api_account import DmApiAccount


def test_post_v1_account():
    api = DmApiAccount(host="http://localhost:5051")
    json = {
        "login": "admin8",
        "email": "admin8@test.ru",
        "password": "admin88"
    }
    response = api.account.post_v1_account(
        json=json
    )
    print(response)
