import allure
from hamcrest import assert_that, has_entries


@allure.title('Проверка авторизации активированного пользователя')
def test_post_v1_account_login(dm_api_facade, orm_db, prepare_user, assertions):
    """
    Тест проверяет создание, активацию и авторизацию пользователя в БД
    """
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    orm_db.delete_user_by_login(login=login)
    dm_api_facade.mailhog.delete_all_messages()
    dataset = orm_db.get_user_by_login(login=login)
    assert len(dataset) == 0
    assertions.check_user_was_created(login=login)
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
            "login": "admin1",
            "roles": ["Guest", "Player"],
            "rating": ({
                "enabled": True,
                "quality": 0,
                "quantity": 0
            })

        }
    ))
    orm_db.db.close_connection()
