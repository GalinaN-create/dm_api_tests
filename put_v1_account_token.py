import requests

url = "http://localhost:5051/v1/account/6007fa5a-b619-48e1-b686-64ba18e8127b"

payload = {}
headers = {
  'X-Dm-Auth-Token': '',
  'X-Dm-Bb-Render-Mode': '',
  'Accept': 'text/plain'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
