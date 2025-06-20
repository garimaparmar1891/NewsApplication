import requests
from utils.token_storage import get_token

BASE_URL = "http://localhost:5000"

def authorized_request(method, endpoint, **kwargs):
    """
    Makes an authorized HTTP request to the server using the JWT token.
    
    Parameters:
    - method (str): HTTP method (GET, POST, etc.)
    - endpoint (str): API endpoint path
    - kwargs: Additional parameters (headers, json, params, etc.)
    
    Returns:
    - Response object from the requests library
    """
    headers = kwargs.get("headers", {})
    token = get_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    kwargs["headers"] = headers
    url = f"{BASE_URL}{endpoint}"
    response = requests.request(method, url, **kwargs)
    return response
