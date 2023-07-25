from services.dm_api_account import Facade
from generic.helpers.mailhog import MailhogApi
from dm_api_account.models.user_envelope import UserRole
from dm_api_account.models.registration_model import Registration
import time
import structlog
from hamcrest import assert_that, has_properties, empty, not_, instance_of, all_of

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_token():
    mailhog = MailhogApi(host="http://localhost:5025")
    api = Facade(host="http://localhost:5051")

    json1 = Registration(
        login="admin995",
        email="admin995@test.ru",
        password="admin995"
    )
    response = api.account_api.post_v1_account(json=json1)
    print(response)

    time.sleep(4)
    token = mailhog.get_token_from_last_email()
    response = api.account_api.put_v1_account_token(token=token)
    assert_that(response.resource, has_properties(
            {"login": "admin995",
             "roles": [UserRole.guest, UserRole.player],
             "rating": has_properties({
                 "enabled": instance_of(bool)
             })

             }
    )
                )
        # has_properties({
        #     "roles": not_(empty())
        # }),
        # has_properties({
        #     "rating": has_properties({
        #         "enabled": instance_of(bool)
        #     })
    #     })
    # ))

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
