import allure
from hamcrest import assert_that, has_properties, instance_of
from dm_api_account.models.user_envelope import UserRole


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
        login=login, oldPassword=password, newPassword=new_password
    )
    assert_that(response.resource, has_properties(
        {"login": "admin1",
         "roles": [UserRole.guest, UserRole.player],
         "rating": has_properties({
             "enabled": instance_of(bool)
         })
         }))
    orm_db.db.close_connection()
