import allure

from dm_api_account.apis.login_api import LoginCredentials


class Login:

    def __init__(self, facade):
        self.facade = facade

        # Проставление заголовков в клиент

    def set_headers(self, headers):
        self.facade.login_api.client.session.headers.update(headers)

    def login_user(self, login: str, password: str, remember_me: bool = True):
        with allure.step('Авторизация юзера'):
            response = self.facade.login_api.post_v1_account_login(
                json=LoginCredentials(
                    login=login,
                    password=password,
                    rememberMe=remember_me
                )
            )
        return response

    def get_auth_token(self, login: str, password: str, remember_me: bool = True):
        with allure.step('Получение авторизационного токена'):
            response = self.login_user(login=login, password=password, remember_me=remember_me)
            token = {'X-Dm-Auth-Token': response.headers['X-Dm-Auth-Token']}
        return token

    def logout_user(self, **kwargs):
        with allure.step('Разлогинивание пользователя'):
            response = self.facade.login_api.delete_v1_account_login(**kwargs)
        return response

    def logout_user_from_all_devices(self, **kwargs):
        with allure.step('Разлогинивание пользователя на всех девайсах'):
            response = self.facade.login_api.delete_v1_account_login_all(**kwargs)
        return response
