import allure
from hamcrest import assert_that, has_properties, instance_of
from apis.dm_api_account.models.user_envelope import UserRole


@allure.suite('Проверка смены почты зареганного пользователя')
@allure.title('Смена почты зареганного пользователя')
def test_put_v1_account_email(dm_api_facade, orm_db, prepare_user, assertions):
    """
    Тест проверяет изменение адреса электронной почты зарегистрированного пользователя
    """
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    orm_db.delete_user_by_login(login=login)
    dataset = orm_db.get_user_by_login(login=login)
    assert len(dataset) == 0
    dm_api_facade.mailhog.delete_all_messages()
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
    response = dm_api_facade.account.change_email(
        login=login,
        email=email,
        password=password
    )
    assert_that(response.resource, has_properties(
        {"login": "admin1",
         "roles": [UserRole.guest, UserRole.player],
         "rating": has_properties({
             "enabled": instance_of(bool)
         })
         }
    )
                )
    orm_db.db.close_connection()
