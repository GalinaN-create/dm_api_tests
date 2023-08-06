from hamcrest import assert_that, has_entries


def test_post_v1_account_login(dm_api_facade, orm_db):
    login = "admin807"
    email = "admin807@test.ru"
    password = "admin807"

    orm_db.delete_user_by_login(login=login)

    dataset = orm_db.get_user_by_login(login=login)
    assert len(dataset) == 0

    dm_api_facade.mailhog.delete_all_messages()

    dataset = orm_db.get_user_by_login(login=login)
    for row in dataset:
        assert row.Login == login, f'User {login} not registered'
    dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    dm_api_facade.account.activate_registered_user(login=login)

    response = dm_api_facade.login.login_user(
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
    orm_db.db.close_connection()
