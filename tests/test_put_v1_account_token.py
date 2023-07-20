import json

import requests
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
from dm_api_account.models.user_envelope import UserRole
from dm_api_account.models.registration_model import Registration
import time
import structlog
from hamcrest import assert_that, has_properties, empty, not_, starts_with

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_token():
    mailhog = MailhogApi(host="http://localhost:5025")
    api = DmApiAccount(host="http://localhost:5051")
    #
    # json1 = Registration(
    #     login="admin400",
    #     email="admin400@test.ru",
    #     password="admin400"
    # )
    # response = api.account.post_v1_account(json=json1)
    # print(response)
    #
    # time.sleep(4)
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
    assert_that(response.resource, has_properties(
        {"login": "admin400",
         "roles": [UserRole.guest, UserRole.player]
         }
    ))
    assert_that(response.resource.roles, not_(empty()))
    assert_that(response.resource.login, starts_with("admin"))
    # expected_json = {
    #     "resource": {
    #         "login": "admin224",
    #         "rating": {
    #             "enabled": True,
    #             "quality": 0,
    #             "quantity": 0
    #         },
    #         "roles": [
    #             "Guest",
    #             "Player"
    #         ]
    #     }
    # }
    #
    # actual_json = json.loads(response.json(by_alias=True, exclude_none=True))
    # assert actual_json == expected_json
