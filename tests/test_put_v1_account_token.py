from dm_api_account.models.user_envelope import UserRole
from hamcrest import assert_that, has_properties, instance_of


def test_put_v1_account_token(dm_api_facade, orm_db):
    login = "admin804"
    email = "admin804@test.ru"
    password = "admin804"

    orm_db.delete_user_by_login(login=login)

    dataset = orm_db.get_user_by_login(login=login)
    assert len(dataset) == 0

    dm_api_facade.mailhog.delete_all_messages()

    dataset = orm_db.get_user_by_login(login=login)
    for row in dataset:
        assert row['Login'] == login, f'User {login} not registered'

    dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    response = dm_api_facade.account.activate_registered_user(login=login)

    assert_that(response.resource, has_properties(
        {"login": "admin804",
         "roles": [UserRole.guest, UserRole.player],
         "rating": has_properties({
             "enabled": instance_of(bool)
         })

         }
    )
                )
    orm_db.db.close_connection()

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
