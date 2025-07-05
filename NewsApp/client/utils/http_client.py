import requests
from utils.token_storage import TokenStorage
from utils.endpoints import BASE_URL

class HttpClient:
    """Handles authorized HTTP requests."""

    @staticmethod
    def authorized_request(method, endpoint, **kwargs):
        headers = kwargs.get("headers", {})
        token = TokenStorage.get_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        kwargs["headers"] = headers
        url = f"{BASE_URL}{endpoint}"
        response = requests.request(method, url, **kwargs)
        return response