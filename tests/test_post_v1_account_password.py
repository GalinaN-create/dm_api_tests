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

    login = "admin921"
    email = "admin921@test.ru"
    password = "admin921"
    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    api.account.activate_registered_user(login=login)

    api.login.login_user(
        login=login,
        password=password
    )
    token = api.login.get_auth_token(login=login, password=password)

    api.account.set_headers(headers=token)
    response = api.account.reset_password(
        login=login,
        email=email
    )

    assert_that(response.json.resource, has_properties(
        {"login": "admin921",
         "roles": [UserRole.guest, UserRole.player],
         "rating": has_properties({
             "enabled": instance_of(bool)
         })
         })

                )
    return response
