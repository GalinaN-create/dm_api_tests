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


@pytest.mark.parametrize('login, email, password, status_code, check', [
    ('login', 'login@mail.ru', random_string(5, 5),
     400, {'Password': ['Short']}),  # длина пароля более 5 символов
    (random_string(1, 1), 'loginn@mail.ru', random_string(1, 1),
     400, {"Login": ['Short'], 'Password': ['Short']}),  # длина логина 1 символ и дляна пароля 1 символ
    ('12345', '12345@mail.ru', '1234567890', 201, ''),  # валидные данные
    ('!!!', '!!!!!!!.!!', '!!!!!!', 400, {'Email': ['Invalid']}),  # Валидация эмейла
    ('', '22@12.ru', '222222', 400, {'Login': ['Empty', 'Short']}),  # Пустое поле логин
])
def test_create_and_activated_user_with_random_params(dm_api_facade, orm_db, login, email, password, status_code,
                                                      check):
    orm_db.delete_user_by_login(login=login)
    dm_api_facade.mailhog.delete_all_messages()
    response = dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password,
        status_code=status_code
    )
    if status_code == 201:
        dataset = orm_db.get_user_by_login(login=login)
        for row in dataset:
            assert row.Login == login, f'User {login} registered'
            assert row.Activated is False, f'User {login} was not activated'

        # api.account.activate_registered_user(login=login)

        orm_db.activated_new_user(login=login)

        dataset = orm_db.get_user_by_login(login=login)
        for row in dataset:
            assert row.Activated is True, f'User {login} not activated'

        dm_api_facade.login.login_user(
            login=login,
            password=password
        )
    else:
        assert response.json()['errors'] == check, f'поле {check}  не соответствует ответу в ошибке'
    orm_db.db.close_connection()
