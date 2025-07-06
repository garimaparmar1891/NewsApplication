import requests
from utils.token_storage import TokenStorage
from utils.endpoints import BASE_URL

class HttpClient:

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

    @staticmethod
    def safe_json_get(response, key, default=None):
        try:
            return response.json().get(key, default)
        except ValueError:
            return response.text if default is None else default

    @staticmethod
    def safe_extract_data(response, default=None):
        try:
            json_response = response.json()
            if isinstance(json_response, list):
                return json_response
            else:
                return json_response.get("data", default)
        except ValueError:
            return default if default is not None else []
