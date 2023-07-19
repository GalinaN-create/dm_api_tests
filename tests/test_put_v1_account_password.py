import requests
from services.dm_api_account import DmApiAccount
from dm_api_account.models.change_password_model import ChangePassword
from hamcrest import assert_that, has_properties



def test_put_v1_account_password():
    api = DmApiAccount(host="http://localhost:5051")
    json = ChangePassword(
        login="admin317",
        token="c18c62af-6a27-4e5a-ab64-f63285219096",
        oldPassword="admin317",
        newPassword="admin3177"
    )
    response = api.account.put_v1_account_password(json=json)
    assert_that(response.resource.login,
                response.resource.roles,
                response.resource.registration

                )
    print(response)
