import json
from requests import Response, session

class MailhogApi:
    def __init__(self, host="http://localhost:5025", headers=None):
        self.host = host
        self.session = session()

    def get_v2_messages(self, limit: int=50) -> Response:
        response = self.session.get(
            url=f"{self.host}/api/v2/messages",
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
        emails = self.get_v2_messages(limit=1).json()
        token_url = json.loads(emails['items'][0]['Content']['Body'])['ConfirmationLinkUrl']
        token = token_url.split('/')[-1]

        return token


result = MailhogApi().get_token_from_last_email()
# print(result)
