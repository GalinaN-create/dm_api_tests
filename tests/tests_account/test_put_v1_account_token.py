import allure
from dm_api_account.models import UserRole
from hamcrest import assert_that, has_properties, instance_of


@allure.suite('Проверка активации пользователя')
@allure.title('Активация пользователя')
def test_put_v1_account_token(dm_api_facade, orm_db, prepare_user, assertions):
    """
    Тест проверяет создание и активацию нового пользователя через БД
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
    response = dm_api_facade.account.activate_registered_user(login=login)
    print(response)
    # assert_that(response.resource, has_properties(
    #     {"login": "admin1",
    #      "roles": [UserRole.guest, UserRole.player],
    #      "rating": has_properties({
    #          "enabled": instance_of(bool)
    #      })
    #
    #      }
    # )
    #             )
    # orm_db.db.close_connection()
