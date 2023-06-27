import requests
from requests import Response
from ..models.registration_model import registration_model
from ..models.reset_password_model import reset_password
from ..models.change_password_model import change_password
from ..models.change_email_model import change_email


class AccountApi:

    def __init__(self, host):
        self.host = host

    def post_v1_account(self, json: registration_model) -> Response:
        """
        Register new user
        :param json: registration_model
        :return:
        """

        headers = {
            'X-Dm-Auth-Token': '',
            'X-Dm-Bb-Render-Mode': '',
            'Content-Type': 'application/json',
            'Accept': 'text/plain'
        }

        response = requests.request(
            method="POST",
            url=f"{self.host}/v1/account",
            headers=headers,
            json=json
        )
        return response

    def get_v1_account(self):
        """
        Get current user
        :return:
        """

        headers = {
            'X-Dm-Auth-Token': '',
            'X-Dm-Bb-Render-Mode': '',
            'Accept': 'text/plain'
        }

        response = requests.request(
            method="GET",
            url=f"{self.host}/v1/account",
            headers=headers
        )
        return response

    def put_v1_account_token(self):
        """
        Activate registered user
        :return:
        """
        token = '123123123'

        headers = {
            'X-Dm-Auth-Token': '',
            'X-Dm-Bb-Render-Mode': '',
            'Accept': 'text/plain'
        }

        response = requests.request(
            method="PUT",
            url=f"{self.host}/v1/account/{token}",
            headers=headers

        )
        return response

    def post_v1_account_password(self, json: reset_password) -> Response:
        """
        Reset registered user password
        :return:
        """

        headers = {
            'X-Dm-Auth-Token': '',
            'X-Dm-Bb-Render-Mode': '',
            'Content-Type': 'application/json',
            'Accept': 'text/plain'
        }

        response = requests.request(
            method="POST",
            url=f"{self.host}/v1/account/password",
            headers=headers,
            json=json
        )
        return response

    def put_v1_account_password(self, json: change_password) -> Response:
        """
        Change registered user password
        :return:
        """

        headers = {
            'X-Dm-Auth-Token': '',
            'X-Dm-Bb-Render-Mode': '',
            'Content-Type': 'application/json',
            'Accept': 'text/plain'
        }

        response = requests.request(
            method="PUT",
            url=f"{self.host}/v1/account/password",
            headers=headers,
            json=json
        )
        return response

    def put_v1_account_email(self, json: change_email) -> Response:
        """
        Change registered user email
        :return:
        """

        headers = {
            'X-Dm-Auth-Token': '',
            'X-Dm-Bb-Render-Mode': '',
            'Content-Type': 'application/json',
            'Accept': 'text/plain'
        }

        response = requests.request(
            method="PUT",
            url=f"{self.host}/v1/account/email",
            headers=headers,
            json=json
        )
        return response
