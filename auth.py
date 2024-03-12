from dotenv import dotenv_values
import requests
import base64
import json

secrets = dotenv_values(".env")

def get_token():
    url = "https://accounts.spotify.com/api/token"

    to_encode_secrets = secrets["API_KEY"] + ':' + secrets["API_SECRET"]
    byte_data = to_encode_secrets.encode('utf-8')
    encoded_data = str(base64.b64encode(byte_data), 'utf-8')
    form = {
        "grant_type": "client_credentials"
    }

    headers = {
        "Authorization": "Basic " + encoded_data,
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    r = requests.post(url, headers=headers, data = form)

    json_result = json.loads(r.content)
    token = json_result["access_token"]

    print(token)


    