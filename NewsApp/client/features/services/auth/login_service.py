from utils.http_client import HttpClient
from utils.endpoints import LOGIN
from utils.response_handler import handle_data_response
from constants import messages as msg

class LoginService:
    @staticmethod
    def login(email, password):
        response = HttpClient.authorized_request(
            method="POST",
            endpoint=LOGIN,
            json={"email": email, "password": password}
        )
        return handle_data_response(response, msg.LOGIN_FAILED)
