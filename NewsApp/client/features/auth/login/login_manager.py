from utils.token_storage import TokenStorage
from .login_service import LoginService

class LoginManager:
    def login(self):
        email, password = self._prompt_login_credentials()
        response = LoginService.login(email, password)
        return self._handle_login_response(response)

    @staticmethod
    def _prompt_login_credentials():
        email = input("Email: ")
        password = input("Password: ")
        return email, password

    def _handle_login_response(self, response):
        try:
            data = response.json()
        except ValueError:
            print("Login failed: Invalid response format.")
            return None

        if response.ok and "access_token" in data.get("data", {}):
            access_token = data["data"]["access_token"]
            user_info = {
                "username": data["data"].get("username", "User"),
                "role": data["data"].get("role", "User")
            }
            TokenStorage.save_token(access_token)
            TokenStorage.save_user_info(user_info)
            print(f"Login successful. Welcome, {user_info['username']}!")
            return user_info["role"].lower()
        else:
            print("Login failed:", data.get("message", "Unknown error"))
            return None 