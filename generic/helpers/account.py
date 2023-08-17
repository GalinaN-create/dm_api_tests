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
            self.facade.account_api.api_client.default_headers.update(headers)

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
        response = self.facade.account_api.get_current(**kwargs)
        return response

    def reset_password(self, login: str, email: str):
        with allure.step('Сброс пароля'):
            response = self.facade.account_api.reset_password(
                reset_password=ResetPassword(
                    login=login,
                    email=email
                )
            )
        return response

    def change_password(self, login: str, old_password: str, new_password: str):
        with allure.step('Смена пароля'):
            token = self.facade.mailhog.get_token_by_reset_password(login=login)
            response = self.facade.account_api.change_password(
                change_password=ChangePassword(
                    login=login,
                    token=token,
                    old_password=old_password,
                    new_password=new_password
                )
            )
        return response

    def change_email(self, login: str, password: str, email: str):
        with allure.step('Сброс почты'):
            response = self.facade.account_api.change_email(
                change_email=ChangeEmail(
                    login=login,
                    password=password,
                    email=email
                )
            )
        return response
