from services.auth_service import AuthService
from utils.exception_handler import handle_exceptions
from constants import messages
from flask import request
from controllers.base_controller import BaseController

class AuthController(BaseController):
    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()

    @handle_exceptions()
    def signup(self):
        data, error = self._validate_json_data(required_fields=messages.REQUIRED_SIGNUP_FIELDS)
        if error:
            return error
        return self.auth_service.signup(data)

    @handle_exceptions()
    def login(self):
        data, error = self._validate_json_data(required_fields=messages.REQUIRED_LOGIN_FIELDS)
        if error:
            return error
        return self.auth_service.login(data)
