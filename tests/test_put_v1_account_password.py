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
    login = "admin951"
    email = "admin951@test.ru"
    password = "admin951"
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
    token = api.login.get_auth_token(
        login=login,
        password=password)
    api.account.set_headers(
        headers=token
    )

    response = api.account.reset_password(
        login=login,
        email=email
    )
    print(response)

    response = api.account.change_password(
        login=login,
        token=token,
        oldPassword=password,
        newPassword=new_password
    )
    return response

    # assert_that(response.resource, all_of(
    #     has_properties(
    #         {"login": "admin992",
    #          "roles": [UserRole.guest, UserRole.player]
    #          }),
    #     has_properties({
    #         "roles": not_(empty())
    #     }),
    #     has_properties({
    #         "rating": has_properties({
    #             "enabled": instance_of(bool)
    #         })
    #     })
    # ))
