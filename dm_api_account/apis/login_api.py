import requests

from requests import Response
from requests import session
from restclient.restclient import Restclient
from dm_api_account.models import *


class LoginApi:

    def __init__(self, host, headers=None):
        self.host = host
        self.client = Restclient(host=host, headers=headers)
        if headers:
            self.client.session.headers.update(headers)

    def post_v1_account_login(self, json: LoginCredentials, status_code: int,  **kwargs) -> LoginCredentials | Response:
        """
        Authenticate via credentials
        :param status_code:
        :param json login_credentials_model
        :return:
        """

        response = self.client.post(
            path=f"/v1/account/login",
            json=json.validate_request_json(json),
            **kwargs
        )
        if response.status_code == 200:
            return LoginCredentials(**response.json())
        return response

    def delete_v1_account_login(self, **kwargs):
        """
        Logout as current user
        :return:
        """

        response = self.client.delete(
            url=f"/v1/account/login",
            **kwargs
        )
        return response

    def delete_v1_account_login_all(self, **kwargs):
        """
        Logout from every device
        :return:
        """

        response = self.client.delete(
            url=f"/v1/account/login/all",
            **kwargs
        )
        return response
