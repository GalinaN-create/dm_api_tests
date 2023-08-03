import requests
from services.dm_api_account import Facade
from dm_api_account.models.change_password_model import ChangePassword
from hamcrest import assert_that, has_properties, all_of, not_, empty, instance_of
from dm_api_account.models.user_envelope import UserRole
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


# TODO токен из хедеров добавить из след. урока
def test_put_v1_account_password():
    api = Facade(host="http://localhost:5051")
    login = "admin925"
    email = "admin925@test.ru"
    password = "admin925"
    new_password = f'{password}2'

    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    api.account.activate_registered_user(
        login=login
    )

    api.login.login_user(
        login=login,
        password=password
    )
    # Токен для хедера
    token = api.login.get_auth_token(
        login=login,
        password=password)

    api.account.set_headers(
        headers=token
    )

    api.account.reset_password(
        login=login,
        email=email
    )

    response = api.account.change_password(
        login=login,
        oldPassword=password,
        newPassword=new_password
    )

    assert_that(response.resource, has_properties(
        {"login": "admin925",
         "roles": [UserRole.guest, UserRole.player],
         "rating": has_properties({
             "enabled": instance_of(bool)
         })
         }),
                )
    return response
