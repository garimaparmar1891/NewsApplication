from utils.http_client import HttpClient
from utils.endpoints import LOGIN

class LoginService:
    @staticmethod
    def login(email, password):
        response = HttpClient.authorized_request(
            method="POST",
            endpoint=LOGIN,
            json={"email": email, "password": password}
        )
        return response 