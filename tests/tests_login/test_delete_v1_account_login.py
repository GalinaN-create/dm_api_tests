import allure


@allure.suite('Проверка выхода из системы у текущего пользователя')
@allure.title('Выход из системы у текущего пользователя')
def test_delete_v1_account_login(dm_api_facade, orm_db, prepare_user, assertions):
    """
    Тест проверяет выход из системы у текущего пользователя
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
    dm_api_facade.login.login_user(
        login=login,
        password=password
    )
    token = dm_api_facade.login.get_auth_token(login=login, password=password)
    dm_api_facade.login.set_headers(headers=token)
    response = dm_api_facade.login.logout_user(headers=token)
    print(response)

    orm_db.db.close_connection()
