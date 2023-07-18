import time
from dm_api_account.models.registration_model import Registration
from dm_api_account.models.change_email_model import ChangeEmail
import requests
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_email():
    mailhog = MailhogApi(host='http://localhost:5025')
    api = DmApiAccount(host="http://localhost:5051")
    json = Registration(
        login="admin2027",
        password="admin2027admin",
        email="admin2027@admin"
    )
    json2 = ChangeEmail(
        login="admin2027",
        password="admin2027admin",
        email="admin2027@admin"
    )
    response = api.account.post_v1_account(json=json)
    time.sleep(2)

    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)

    response = api.account.put_v1_account_email(json=json2)

    print(response)
