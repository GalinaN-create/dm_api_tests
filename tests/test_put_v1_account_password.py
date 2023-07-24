import requests
from services.dm_api_account import DmApiAccount
from dm_api_account.models.change_password_model import ChangePassword
from hamcrest import assert_that, has_properties, all_of, not_, empty, instance_of
from dm_api_account.models.user_envelope import UserRole


# TODO токен из хедеров добавить из след. урока
def test_put_v1_account_password():
    api = DmApiAccount(host="http://localhost:5051")
    json = ChangePassword(
        login="admin992",
        token="3ef94af1-607a-47cb-a015-d5a01989f10f",
        oldPassword="admin992",
        newPassword="admin9922"
    )
    response = api.account.put_v1_account_password(json=json)
    assert_that(response.resource, all_of(
        has_properties(
            {"login": "admin992",
             "roles": [UserRole.guest, UserRole.player]
             }),
        has_properties({
            "roles": not_(empty())
        }),
        has_properties({
            "rating": has_properties({
                "enabled": instance_of(bool)
            })
        })
    ))