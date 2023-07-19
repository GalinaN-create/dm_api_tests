import json

import requests
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
from dm_api_account.models.user_envelope import UserRole
from dm_api_account.models.registration_model import Registration
import time
import structlog
from hamcrest import assert_that, has_properties

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_token():
    mailhog = MailhogApi(host="http://localhost:5025")
    api = DmApiAccount(host="http://localhost:5051")

    json = Registration(
        login="admin226",
        email="admin226@test.ru",
        password="admin226"
    )
    response = api.account.post_v1_account(json=json)

    time.sleep(4)
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
    assert_that(response.resource, has_properties(
        {"login": "admin226",
         "roles": [UserRole.guest, UserRole.player]
         }
    ))
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
