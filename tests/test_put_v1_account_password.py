import requests
from services.dm_api_account import DmApiAccount


def test_put_v1_account_password():
    api = DmApiAccount(host="http://localhost:5051")
    json = {
        "login": "admin_4",
        "token": "c05cda57-2a12-4442-8105-b88bf0e9eede",
        "oldPassword": "admin_44",
        "newPassword": "admin_4"
    }
    response = api.account.put_v1_account_password(
        json=json
    )
    print(response)
