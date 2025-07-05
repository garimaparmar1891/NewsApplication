from utils.http_client import HttpClient
from utils.endpoints import SIGNUP

class SignupService:
    @staticmethod
    def perform_signup_request(name, email, password):
        return HttpClient.authorized_request(
            method="POST",
            endpoint=SIGNUP,
            json={
                "username": name,
                "email": email,
                "password": password
            }
        )

    @staticmethod
    def handle_signup_response(response):
        if response.ok:
            print("Signup successful.")
        else:
            try:
                print("Signup failed:", response.json().get("message", "Unknown error"))
            except ValueError:
                print("Signup failed: Invalid response from server.") 