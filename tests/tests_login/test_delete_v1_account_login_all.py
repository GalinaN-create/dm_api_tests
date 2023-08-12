import allure


@allure.suite('Проверка выхода из системы со всех устройств')
@allure.title('Выход из системы со всех устройств')
def test_delete_v1_account_login_all(dm_api_facade, orm_db, prepare_user, assertions):
    """
    Тест проверяет выход из системы со всех устройств
    """
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    orm_db.delete_user_by_login(login=login)
    dm_api_facade.mailhog.delete_all_messages()
    dataset = orm_db.get_user_by_login(login=login)
    assert len(dataset) == 0
    dataset = orm_db.get_user_by_login(login=login)
    for row in dataset:
        assert row.Login == login, f'User {login} not registered'
    dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    dm_api_facade.account.activate_registered_user(
        login=login
    )
    dm_api_facade.login.login_user(
        login=login,
        password=password
    )
    token = dm_api_facade.login.get_auth_token(
        login=login,
        password=password)
    dm_api_facade.login.set_headers(
        headers=token
    )
    dm_api_facade.login.logout_user_from_all_devices(
        headers=token
    )
    orm_db.db.close_connection()
