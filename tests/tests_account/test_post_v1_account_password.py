import allure
from hamcrest import assert_that, has_entries, equal_to, all_of, contains_inanyorder


@allure.suite('Проверка сброса пароля зареганного пользователя')
@allure.title('Сброс пароля зареганного пользователя')
def test_post_v1_account_password(dm_api_facade, orm_db, prepare_user, assertions):
    """
    Тест проверяет создание, активацию и сброс пароля активированного пользователя
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
    dm_api_facade.account.set_headers(headers=token)
    response = dm_api_facade.account.reset_password(
        login=login,
        email=email
    )

    assert_that(response['resource']['login'], equal_to("admin1"))

    roles_list = [str(role) for role in response['resource']['roles']]
    assert_that(roles_list, equal_to(['Guest', 'Player']))

    assert_that(response['resource']['rating'], has_entries({
        "enabled": True,
        "quality": 0,
        "quantity": 0
    }))


