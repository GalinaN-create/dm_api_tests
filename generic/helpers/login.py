import allure

from dm_api_account.api.login_api import LoginCredentials


class Login:

    def __init__(self, facade):
        from services.dm_api_account import Facade
        self.facade: Facade = facade

        # Проставление заголовков в клиент

    def set_headers(self, headers):
        self.facade.login_api.api_client.default_headers.update(headers)

    def login_user(self, login: str, password: str, remember_me: bool = True):
        with allure.step('Авторизация юзера'):
            response = self.facade.login_api.v1_account_login_post(
                _return_http_data_only=False,
                login_credentials=LoginCredentials(
                    login=login,
                    password=password,
                    remember_me=remember_me
                )
            )
        return response

    def get_auth_token(self, login: str, password: str, remember_me: bool = True):
        with allure.step('Получение авторизационного токена'):
            response = self.login_user(login=login, password=password, remember_me=remember_me)
            print(response)
            token = {'X-Dm-Auth-Token': response[2]['X-Dm-Auth-Token']}
        return token

    def logout_user(self, **kwargs):
        with allure.step('Разлогинивание пользователя'):
            response = self.facade.login_api.v1_account_login_delete(**kwargs)

        return response

    def logout_user_from_all_devices(self, **kwargs):
        with allure.step('Разлогинивание пользователя на всех девайсах'):
            response = self.facade.login_api.v1_account_login_all_delete(**kwargs)
        return response
