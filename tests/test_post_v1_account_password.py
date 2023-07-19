import requests
from services.dm_api_account import DmApiAccount
from hamcrest import assert_that, has_properties
from dm_api_account.models.user_envelope import UserRole
import structlog
from dm_api_account.models.reset_password_model import ResetPassword

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_password():
    api = DmApiAccount(host="http://localhost:5051")
    json = ResetPassword(
        login="admin316",
        email="admin316@test.ru"
    )
    response = api.account.post_v1_account_password(json=json)
    assert_that(response, has_properties(
        {
                "Login": "admin316",
                "roles": [UserRole.guest, UserRole.player]

        }
    ))

    print(response)
