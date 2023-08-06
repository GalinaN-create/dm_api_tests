from generic.helpers.dm_db import DmDatabase
from generic.helpers.orm_db import OrmDatabase
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
    api = Facade(host="http://localhost:5051")
    login = "admin804"
    email = "admin804@test.ru"
    password = "admin804"
    orm = OrmDatabase(user='postgres', password='admin', host='localhost', database='dm3.5')

    orm.delete_user_by_login(login=login)

    dataset = orm.get_user_by_login(login=login)
    assert len(dataset) == 0

    api.mailhog.delete_all_messages()

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row['Login'] == login, f'User {login} not registered'

    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    response = api.account.activate_registered_user(login=login)

    assert_that(response.resource, has_properties(
        {"login": "admin804",
         "roles": [UserRole.guest, UserRole.player],
         "rating": has_properties({
             "enabled": instance_of(bool)
         })

         }
    )
                )
    orm.db.close_connection()

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
