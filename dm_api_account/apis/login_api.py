import requests


class LoginApi():

    def __init__(self, host):
        self.host = host

    def post_v1_account_login(self):
        """
        Authenticate via credentials
        :return:
        """

        payload = {
            "login": "admin",
            "password": "adminadmin",
            "rememberMe": False
        }
        headers = {
            'X-Dm-Bb-Render-Mode': '',
            'Content-Type': 'application/json',
            'Accept': 'text/plain'
        }

        response = requests.request(
            method="POST",
            url=f"{self.host}/v1/account/login",
            headers=headers,
            json=payload
        )
        return response

    def delete_v1_account_login(self):
        """
        Logout as current user
        :return:
        """

        headers = {
            'X-Dm-Auth-Token': '',
            'X-Dm-Bb-Render-Mode': '',
            'Accept': 'text/plain'
        }

        response = requests.request(
            method="DELETE",
            url=f"{self.host}/v1/account/login",
            headers=headers
        )
        return response

    def delete_v1_account_login_all(self):
        """
        Logout from every device
        :return:
        """

        headers = {
            'X-Dm-Auth-Token': '',
            'X-Dm-Bb-Render-Mode': '',
            'Accept': 'text/plain'
        }

        response = requests.request(
            method="DELETE",
            url=f"{self.host}/v1/account/login/all",
            headers=headers
        )
        return response