import time

from generic.helpers.dm_db import DmDatabase
from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade
from generic.helpers.mailhog import MailhogApi
import structlog
from dm_api_account.models.registration_model import Registration
from dm_api_account.models.login_credentials_model import LoginCredentials
from hamcrest import assert_that, has_properties, instance_of, all_of, not_, empty, has_entries
from dm_api_account.models.user_envelope import UserRole

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


# TODO Готово
def test_post_v1_account_login():
    api = Facade(host="http://localhost:5051")

    login = "admin807"
    email = "admin807@test.ru"
    password = "admin807"

    orm = OrmDatabase(user='postgres', password='admin', host='localhost', database='dm3.5')

    orm.delete_user_by_login(login=login)

    dataset = orm.get_user_by_login(login=login)
    assert len(dataset) == 0

    api.mailhog.delete_all_messages()

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Login == login, f'User {login} not registered'
    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    api.account.activate_registered_user(login=login)

    response = api.login.login_user(
        login=login,
        password=password
    )

    assert_that(response.json()['resource'], has_entries(
        {
            "login": "admin807",
            "roles": ["Guest", "Player"],
            "rating": ({
                "enabled": True,
                "quality": 0,
                "quantity": 0
            })

        }
    ))
    orm.db.close_connection()


