from dm_api_account.models.registration_model import Registration
from dm_api_account.models.change_email_model import ChangeEmail
from services.dm_api_account import Facade
from generic.helpers.mailhog import MailhogApi
import structlog
from hamcrest import assert_that, has_properties, all_of, not_, empty, instance_of
from dm_api_account.models.user_envelope import UserRole

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


# TODO готов
def test_put_v1_account_email():
    api = Facade(host="http://localhost:5051")
    login = "admin920"
    email = "admin920@test.ru"
    password = "admin920"

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

    response = api.account.change_email(
        login=login,
        email=email,
        password=password
    )
    assert_that(response.resource, has_properties(
        {"login": "admin920",
         "roles": [UserRole.guest, UserRole.player],
         "rating": has_properties({
             "enabled": instance_of(bool)
         })
         }
    )
                )

