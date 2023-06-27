import requests


class AccountApi:

    def __init__(self, host):
        self.host = host

    def post_v1_account(self):
        """
        Register new user
        :return:
        """

        payload = {
            "login": "admin5",
            "email": "admin1@test.ru",
            "password": "admin55"
        }
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

    def post_v1_account_password(self):
        """
        Reset registered user password
        :return:
        """

        payload = {
            "login": "login_4",
            "email": "login_4@login"
        }
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
            json=payload
        )
        return response

    def put_v1_account_password(self):
        """
        Change registered user password
        :return:
        """

        payload = {
            "login": "admin_4",
            "token": "c05cda57-2a12-4442-8105-b88bf0e9eede",
            "oldPassword": "admin_44",
            "newPassword": "admin_4"
        }
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
            json=payload
        )
        return response

    def put_v1_account_email(self):
        """
        Change registered user email
        :return:
        """

        payload = {
            "login": "admin",
            "password": "adminadmin",
            "email": "admin@admin"
        }
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
            json=payload
        )
        return response