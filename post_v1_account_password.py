import requests

"""

"""
url = "http://localhost:5051/v1/account/password"

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
    url=url,
    headers=headers,
    json=payload
)
