import allure
from hamcrest import assert_that, has_properties, instance_of, equal_to, has_entries
from dm_api_account.models import UserRole


@allure.suite('Проверка смены пароля зареганного пользователя')
@allure.title('Смена пароля зареганного пользователя')
def test_put_v1_account_password(dm_api_facade, orm_db, prepare_user, assertions):
    """
    Тест проверяет возможность изменения пароля у зарегистрированного пользователя через БД
    """
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    new_password = f'{password}2'
    orm_db.delete_user_by_login(login=login)
    dm_api_facade.mailhog.delete_all_messages()
    dataset = orm_db.get_user_by_login(login=login)
    assert len(dataset) == 0
    assertions.check_user_was_created(login=login)
    dm_api_facade.account.register_new_user(
        login=login, email=email, password=password
    )
    dm_api_facade.account.activate_registered_user(
        login=login
    )
    dm_api_facade.login.login_user(
        login=login, password=password
    )
    # Токен для хедера
    token = dm_api_facade.login.get_auth_token(
        login=login, password=password
    )
    dm_api_facade.account.set_headers(
        headers=token
    )
    dm_api_facade.account.reset_password(
        login=login, email=email
    )
    response = dm_api_facade.account.change_password(
        login=login, old_password=password, new_password=new_password
    )
    print(response)
    assert_that(response['resource']['login'], equal_to("admin1"))

    roles_list = [str(role) for role in response['resource']['roles']]
    assert_that(roles_list, equal_to(['Guest', 'Player']))

    assert_that(response['resource']['rating'], has_entries({
        "enabled": True,
        "quality": 0,
        "quantity": 0
    }))
    orm_db.db.close_connection()
