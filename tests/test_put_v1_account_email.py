from dm_api_account.models.registration_model import Registration
from dm_api_account.models.change_email_model import ChangeEmail
from services.dm_api_account import DmApiAccount
from generic.helpers.mailhog import MailhogApi
import structlog
from hamcrest import assert_that, has_properties, all_of, not_, empty, instance_of
from dm_api_account.models.user_envelope import UserRole
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)

#TODO готов
def test_put_v1_account_email():
    mailhog = MailhogApi(host='http://localhost:5025')
    api = DmApiAccount(host="http://localhost:5051")
    json = Registration(
        login="admin997",
        email="admin997@test.ru",
        password="admin997"
    )
    json2 = ChangeEmail(
        login="admin997",
        password="admin997",
        email="admin9977@test.ru"
    )
    response = api.account_api.post_v1_account(json=json)

    response = api.account_api.put_v1_account_email(json=json2)
    assert_that(response.resource, all_of(
        has_properties(
            {"login": "admin997",
             "roles": [UserRole.guest, UserRole.player]
             }),
        has_properties({
            "roles": not_(empty())
        }),
        has_properties({
            "rating": has_properties({
                "enabled": instance_of(bool)
            })
        })
    ))
