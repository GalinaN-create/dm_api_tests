import requests
from services.dm_api_account import DmApiAccount
from hamcrest import assert_that, has_entries
from dm_api_account.models.user_envelope import UserRole
import structlog
from dm_api_account.models.reset_password_model import ResetPassword

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_password():
    api = DmApiAccount(host="http://localhost:5051")
    json = ResetPassword(
        login="admin400",
        email="admin400@test.ru"
    )
    response = api.account.post_v1_account_password(json=json)

    assert_that(response.json(), has_entries(
        {
            "resource": has_entries({"login": "admin400",
                                     "roles": ['Guest', 'Player']}),
            "metadata": has_entries({"email": "ad..0@te..u"})
        }
    ))




    #
    #             )

    print(response)
