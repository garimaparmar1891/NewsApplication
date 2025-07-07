from utils.input_utils import get_non_empty_input
from utils.token_storage import TokenStorage
import getpass

EMAIL_PROMPT = "Email: "
PASSWORD_PROMPT = "Password: "
ACCESS_TOKEN_KEY = "access_token"

class LoginHandler:
    @staticmethod
    def login():
        try:
            email, password = LoginHandler._get_credentials()
            return LoginHandler._process_login(email, password)
        except Exception as e:
            print(f"Login process failed: {str(e)}")
            return None

    @staticmethod
    def _get_credentials():
        try:
            email = get_non_empty_input(EMAIL_PROMPT)
            password = getpass.getpass(PASSWORD_PROMPT)
            return email, password
        except Exception:
            raise

    @staticmethod
    def _process_login(email, password):
        from features.services.auth.login_service import LoginService
        
        try:
            success, data = LoginService.login(email, password)
            if not success:
                print("Invalid email or password. Please try again.\n")
                return None
                
            if LoginHandler._is_valid_response(data):
                return LoginHandler._handle_success(data)
            else:
                return None
                
        except Exception:
            return None

    @staticmethod
    def _is_valid_response(data):
        return isinstance(data, dict) and ACCESS_TOKEN_KEY in data

    @staticmethod
    def _handle_success(data):
        try:
            access_token = data[ACCESS_TOKEN_KEY]
            user_info = LoginHandler._extract_user_info(data)
            LoginHandler._save_user_data(access_token, user_info)
            return user_info["role"].lower()
        except Exception:
            return None

    @staticmethod
    def _extract_user_info(data):
        return {
            "username": data.get("username", "User"),
            "role": data.get("role", "User")
        }

    @staticmethod
    def _save_user_data(access_token, user_info):
        try:
            TokenStorage.save_token(access_token)
            TokenStorage.save_user_info(user_info)
        except Exception:
            raise
