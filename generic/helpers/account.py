from dm_api_account.models.registration_model import Registration
from generic.helpers.mailhog import MailhogApi


class Account:
    def __init__(self, facade):
        self.facade = facade

    def register_new_user(self, login: str, email: str, password: str):
        response = self.facade.account_api.post_v1_account(
            json=Registration(
                login=login,
                email=email,
                password=password
            )
        )
        return response

    def activate_register_user(self, token: str):
        token = mailhog.get_token_from_last_email()
        response = self.facade.account_api.put_v1_account_token(token=token)
