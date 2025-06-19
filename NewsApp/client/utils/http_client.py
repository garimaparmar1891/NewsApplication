import requests

BASE_URL = "http://127.0.0.1:5000"

def authorized_request(method, endpoint, **kwargs):
    url = BASE_URL + endpoint

    response = requests.request(method, url, **kwargs)
    return response
