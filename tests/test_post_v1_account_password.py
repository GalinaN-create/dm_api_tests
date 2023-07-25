import requests
from services.dm_api_account import DmApiAccount
from hamcrest import assert_that, all_of, has_properties, not_, empty, instance_of
from dm_api_account.models.user_envelope import UserRole
import structlog
from dm_api_account.models.reset_password_model import ResetPassword

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


# TODO готов
def test_post_v1_account_password():
    api = DmApiAccount(host="http://localhost:5051")
    json = ResetPassword(
        login="admin992",
        email="admin992@test.ru"
    )
    response = api.account_api.post_v1_account_password(json=json)

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
