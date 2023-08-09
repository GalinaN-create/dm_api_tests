import allure
import pytest
from hamcrest import assert_that, has_entries
from string import ascii_letters, digits
import random


def random_string(begin=1, end=10):
    symbols = ascii_letters + digits
    string = ''
    for _ in range(random.randint(begin, end)):
        string += random.choice(symbols)
    return string


class TestsPostV1Account:
    @allure.title('Проверка создания и активации пользователя')
    def test_post_v1_account(
            self,
            dm_api_facade,
            orm_db,
            prepare_user,
            assertions
    ):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        orm_db.delete_user_by_login(login=login)
        dm_api_facade.mailhog.delete_all_messages()
        dm_api_facade.account.register_new_user(login=login, email=email, password=password)
        assertions.check_user_was_created(login=login)
        # api.account.activate_registered_user(login=login)
        orm_db.activated_new_user(login=login)
        assertions.check_user_was_activated(login=login)
        response = dm_api_facade.login.login_user(login=login, password=password)

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

    @pytest.mark.parametrize('login, email, password, status_code, check', [
        ('login', 'login@mail.ru', random_string(5, 5), 400, {'Password': ['Short']}),  # длина пароля более 5 символов
        (random_string(1, 1), 'loginn@mail.ru', random_string(1, 1), 400, {"Login": ['Short'], 'Password': ['Short']}),
        # длина логина 1 символ и дляна пароля 1 символ
        ('12345', '12345@mail.ru', '1234567890', 201, ''),  # валидные данные
        ('!!!', '!!!!!!!.!!', '!!!!!!', 400, {'Email': ['Invalid']}),  # Валидация эмейла
        ('', '22@12.ru', '222222', 400, {'Login': ['Empty', 'Short']}),  # Пустое поле логин
    ])
    @allure.title('Позитивные и негативные проверки на создание и активацию пользователя')
    def test_create_and_activated_user_with_random_params(
            self,
            dm_api_facade,
            orm_db, login,
            email,
            password,
            status_code,
            check,
            assertions
    ):
        """
        Тест проверяет создание, активацию пользователя в БД и логинится
        """
        orm_db.delete_user_by_login(login=login)
        dm_api_facade.mailhog.delete_all_messages()

        response = dm_api_facade.account.register_new_user(login=login, email=email, password=password,
                                                           status_code=status_code)
        if status_code == 201:
            assertions.check_user_was_created(login=login)
            # api.account.activate_registered_user(login=login)
            orm_db.activated_new_user(login=login)
            assertions.check_user_was_activated(login=login)
            dm_api_facade.login.login_user(login=login, password=password)
        else:
            assert response.json()['errors'] == check, f'поле {check}  не соответствует ответу в ошибке'
        orm_db.db.close_connection()

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
