import json
import time

import allure
from requests import Response
from common_libs.restclient.restclient import Restclient


def decorator(fn):
    def _wrapper(*args, **kwargs):
        for i in range(5):
            response = fn(*args, **kwargs)
            emails = response.json()['items']
            if len(emails) < 1:
                print(f'attempt{i}')
                time.sleep(2)
                continue
            else:
                return response

    return _wrapper


class MailhogApi:
    def __init__(self, host="http://localhost:5025"):
        self.host = host
        self.client = Restclient(host=host)

    @decorator
    def get_api_v2_messages(self, limit: int = 50) -> Response:
        """
        Get messages by limit
        :param limit:
        :return:
        """
        with allure.step('Получение сообщений с почты'):
            response = self.client.get(
                path=f"/api/v2/messages",
                params={
                    'limit': limit
                }
            )
        return response

    def get_token_from_last_email(self) -> str:
        """
        Get user activation token from last email
        :return:
        """
        with allure.step('Получение авторизационного токена по почте'):
            emails = self.get_api_v2_messages(limit=1).json()
            token_url = json.loads(emails['items'][0]['Content']['Body'])['ConfirmationLinkUrl']
            token = token_url.split('/')[-1]
        return token

    def get_token_by_reset_password(self, login: str, attempt=5):
        with allure.step('Получение токена из хедера для сброса пароля'):

            if attempt == 0:
                raise AssertionError(f'Не удалось получить письмо с логином {login}')

            emails = self.get_api_v2_messages(limit=100).json()['items']
            for email in emails:
                user_data = json.loads(email['Content']['Body'])
                confirmation_link_uri = user_data.get('ConfirmationLinkUri')
                for key, value in user_data.items():
                    if login == user_data.get('Login') and key == 'ConfirmationLinkUri':
                        token = user_data['ConfirmationLinkUri'].split('/')[-1]
                        print(token)
                        return token
            time.sleep(2)
            print('Попытка получить письмо сброса пароля')
            return self.get_token_by_reset_password(login=login, attempt=attempt - 1)

            self.MailhogApi().get_token_by_reset_password("admin954")

    # self.MailhogApi().get_token_by_reset_password("admin954")

    def get_token_by_login(self, login: str, attempt=10):
        with allure.step('Получение авторизационного токена по логину'):
            if attempt == 0:
                raise AssertionError(f'Не удалось получить письмо с логином {login}')
            emails = self.get_api_v2_messages(limit=100).json()['items']
            for email in emails:
                user_data = json.loads(email['Content']['Body'])
                if login == user_data.get('Login'):
                    token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                    print(token)
                    return token
            time.sleep(2)
        return self.get_token_by_login(login=login, attempt=attempt - 1)

    # if __name__ == '__main__':
    #     MailhogApi().get_token_by_login("admin994")

    def delete_all_messages(self):
        with allure.step('Зачистка почты'):
            response = self.client.delete(path='/api/v1/messages')
        return response
