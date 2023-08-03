import time

from services.dm_api_account import Facade
from generic.helpers.mailhog import MailhogApi
import structlog
from dm_api_account.models.registration_model import Registration
from dm_api_account.models.login_credentials_model import LoginCredentials
from hamcrest import assert_that, has_properties, instance_of, all_of, not_, empty
from dm_api_account.models.user_envelope import UserRole

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


# TODO Готово
def test_post_v1_account_login():
    api = Facade(host="http://localhost:5051")

    login = "admin950"
    email = "admin950@test.ru"
    password = "admin950"

    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    api.account.activate_registered_user(login=login)

    response = api.login.login_user(
        login=login,
        password=password
    )

    assert_that(response.resource, has_properties(
        {
            "login": "admin992",
            "roles": [UserRole.guest, UserRole.player],
            "rating": has_properties({
                "enabled": instance_of(bool)
            })

        }
    ))

    return response
