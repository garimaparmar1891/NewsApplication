import requests
from utils.token_storage import get_token
from utils.endpoints import BASE_URL

def authorized_request(method, endpoint, **kwargs):
    headers = kwargs.get("headers", {})
    token = get_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    kwargs["headers"] = headers
    url = f"{BASE_URL}{endpoint}"
    response = requests.request(method, url, **kwargs)
    return response
