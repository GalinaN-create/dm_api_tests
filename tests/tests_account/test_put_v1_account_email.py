import allure
from hamcrest import assert_that, has_properties, instance_of, equal_to, has_entries
from dm_api_account.models import UserRole


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
    print(response)
    # assert_that(response.resource, has_properties(
    #     {"login": "admin1",
    #      "roles": [UserRole.guest, UserRole.player],
    #      "rating": has_properties({
    #          "enabled": instance_of(bool)
    #      })
    #      }
    # )
    #             )

    assert_that(response['resource']['login'], equal_to("admin1"))

    roles_list = [str(role) for role in response['resource']['roles']]
    assert_that(roles_list, equal_to(['Guest', 'Player']))

    assert_that(response['resource']['rating'], has_entries({
        "enabled": True,
        "quality": 0,
        "quantity": 0
    }))
    orm_db.db.close_connection()
