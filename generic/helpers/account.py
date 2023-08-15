import allure

from dm_api_account.models import Registration

from dm_api_account.models import ChangePassword
from dm_api_account.models import ResetPassword
from dm_api_account.models import ChangeEmail


class Account:
    def __init__(self, facade):
        from services.dm_api_account import Facade
        self.facade: Facade = facade

    # Проставление заголовков в клиент
    def set_headers(self, headers):
        with allure.step('Проставление заголовков в клиент'):
            self.facade.account_api.client.session.headers.update(headers)

    def register_new_user(
            self,
            login: str,
            email: str,
            password: str
    ):
        response = self.facade.account_api.register(
            registration=Registration(
                login=login,
                email=email,
                password=password
            )

        )
        return response

    def activate_registered_user(self, login: str):
        with allure.step('Активация нового пользователя'):
            token = self.facade.mailhog.get_token_by_login(login=login)
            response = self.facade.account_api.activate(
                token=token
            )
        return response

    def get_current_user_info(self, **kwargs):
        response = self.facade.account_api.get_v1_account(**kwargs)
        return response

    def reset_password(self, login: str, email: str):
        with allure.step('Сброс пароля'):
            response = self.facade.account_api.post_v1_account_password(
                json=ResetPassword(
                    login=login,
                    email=email
                )
            )
        return response

    def change_password(self, login: str, oldPassword: str, newPassword: str):
        with allure.step('Смена пароля'):
            token = self.facade.mailhog.get_token_by_reset_password(login=login)
            response = self.facade.account_api.put_v1_account_password(
                json=ChangePassword(
                    login=login,
                    token=token,
                    oldPassword=oldPassword,
                    newPassword=newPassword
                )
            )
        return response

    def change_email(self, login: str, password: str, email: str):
        with allure.step('Сброс почты'):
            response = self.facade.account_api.put_v1_account_email(
                json=ChangeEmail(
                    login=login,
                    password=password,
                    email=email
                )
            )
        return response
