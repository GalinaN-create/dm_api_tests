from hamcrest import assert_that, has_entries


def test_post_v1_account(dm_api_facade, orm_db, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    orm_db.delete_user_by_login(login=login)
    dm_api_facade.mailhog.delete_all_messages()
    dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    dataset = orm_db.get_user_by_login(login=login)
    for row in dataset:
        assert row.Login == login, f'User {login} registered'
        assert row.Activated is False, f'User {login} was not activated'

    # api.account.activate_registered_user(login=login)

    orm_db.activated_new_user(login=login)

    dataset = orm_db.get_user_by_login(login=login)
    for row in dataset:
        assert row.Activated is True, f'User {login} not activated'

    response = dm_api_facade.login.login_user(
        login=login,
        password=password
    )

    assert_that(response.json()['resource'], has_entries(
        {
            "login": 'admin1',
            "roles": ["Guest", "Player"],
            "rating": ({
                "enabled": True,
                "quality": 0,
                "quantity": 0
            })

        }
    ))

    #
    #
    # def check_input_json(json):
    #     for key, value in json.items():
    #         if key == 'login':
    #             assert isinstance(value, str), f'Тип значения в ключе {key} должен быть str, но получен {type(value)}'
    #         if key == 'email':
    #             assert isinstance(value, str), f'Тип значения в ключе {key} должен быть str, но получен {type(value)}'
    #         if key == 'password':
    #             assert isinstance(value, str), f'Тип значения в ключе {key} должен быть равен str, но получен {type(value)}'
