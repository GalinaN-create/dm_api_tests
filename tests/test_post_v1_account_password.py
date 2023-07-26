import requests
from services.dm_api_account import Facade
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
    api = Facade(host="http://localhost:5051")

    login = "admin945"
    email = "admin945@test.ru"
    password = "admin945"
    response = api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    api.account.activate_registered_user(login=login)

    response = api.login.login_user(
        login=login,
        password=password
    )
    return response

    api.account.set_headers(headers=token)
    api.account.reset_password(
        login=login,
        email=email
    )
    return response

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
