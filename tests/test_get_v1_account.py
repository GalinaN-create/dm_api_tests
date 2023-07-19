import requests
from services.dm_api_account import DmApiAccount
import structlog
from hamcrest import assert_that, has_properties
from dm_api_account.models.user_envelope import UserRole

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_get_v1_account():
    api = DmApiAccount(host="http://localhost:5051")
    response = api.account.get_v1_account()
    assert_that(response.resource.login,
                response.resource.roles,
                response.resource.registration

                )
    print(response)
