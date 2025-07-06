from utils.http_client import HttpClient
from utils.endpoints import SIGNUP
from utils.response_handler import handle_response
from constants.messages import SIGNUP_SUCCESS, SIGNUP_FAILED

class SignupService:
    @staticmethod
    def signup(email, password, name):
        response = HttpClient.authorized_request(
            method="POST",
            endpoint=SIGNUP,
            json={"email": email, "password": password, "name": name}
        )
        return handle_response(
            response,
            SIGNUP_SUCCESS,
            SIGNUP_FAILED
        )
