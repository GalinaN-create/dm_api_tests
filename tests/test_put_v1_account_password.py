import requests
from services.dm_api_account import DmApiAccount
from dm_api_account.models.change_password_model import ChangePassword
from hamcrest import assert_that, has_entries


def test_put_v1_account_password():
    api = DmApiAccount(host="http://localhost:5051")
    json = ChangePassword(
        login="admin400",
        token="9f70426d-332e-4417-9d77-94929fa45330",
        oldPassword="admin400",
        newPassword="admin4000"
    )
    response = api.account.put_v1_account_password(json=json)
    assert_that(response.json(), has_entries(
        {
            "resource": has_entries({"login": "admin4000",
                                     "roles": ['Guest', 'Player'],
                                     "rating": {"enabled": True, "quality": 0, "quantity": 0}
                                     })

        }
    ))
    print(response)
