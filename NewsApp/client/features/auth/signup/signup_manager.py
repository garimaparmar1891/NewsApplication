from features.auth.signup.signup_service import SignupService

class SignupManager:
    @staticmethod
    def signup():
        name, email, password = SignupManager.prompt_signup_details()
        response = SignupService.perform_signup_request(name, email, password)
        SignupService.handle_signup_response(response)

    @staticmethod
    def prompt_signup_details():
        name = input("Name: ")
        email = input("Email: ")
        password = input("Password: ")
        return name, email, password 