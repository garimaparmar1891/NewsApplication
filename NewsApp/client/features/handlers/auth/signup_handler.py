from features.services.auth.signup_service import SignupService
from utils.input_utils import get_non_empty_input

SIGNUP_NAME_PROMPT = "Name: "
SIGNUP_EMAIL_PROMPT = "Email: "
SIGNUP_PASSWORD_PROMPT = "Password: "

class SignupHandler:
    @staticmethod
    def signup():
        try:
            name, email, password = SignupHandler._get_user_details()
            success, message = SignupService.signup(email, password, name)

            return success, message
            
        except Exception as e:
            error_message = f"Signup failed due to an unexpected error: {str(e)}"
            return False, error_message

    @staticmethod
    def _get_user_details():
        try:
            name = get_non_empty_input(SIGNUP_NAME_PROMPT)
            email = get_non_empty_input(SIGNUP_EMAIL_PROMPT)
            password = get_non_empty_input(SIGNUP_PASSWORD_PROMPT)
            return name, email, password
        except Exception as e:
            error_message = f"Failed to get user details: {str(e)}"
            raise Exception(error_message)
