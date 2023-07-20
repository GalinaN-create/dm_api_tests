import time
from dm_api_account.models.registration_model import Registration
from dm_api_account.models.change_email_model import ChangeEmail
import requests
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog
from hamcrest import assert_that, has_properties, has_entries
from dm_api_account.models.user_envelope import UserRole
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_email():
    mailhog = MailhogApi(host='http://localhost:5025')
    api = DmApiAccount(host="http://localhost:5051")

    json2 = ChangeEmail(
        login="admin400",
        password="admin400",
        email="admin400@test.ru"
    )
    # response = api.account.post_v1_account(json=json)

    response = api.account.put_v1_account_email(json=json2)
    # assert_that(response.resource, has_properties(
    #     {
    #         "login": "admin316",
    #         "roles": [UserRole.guest, UserRole.player],
    #
    #
    #     }
    # ))
    assert_that(response.json(), has_entries(
        {
            "resource": has_entries({"login": "admin400",
                                     "roles": ['Guest', 'Player'],
                                     "rating": {"enabled": True, "quality": 0, "quantity": 0}
                                     })

        }
    ))
    print(response)
