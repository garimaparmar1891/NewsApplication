import re
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from repositories.auth_repository import AuthRepository
from repositories.login_history_repository import LoginHistoryRepository
from http import HTTPStatus
from datetime import timedelta
from constants import messages
from utils.custom_exceptions import AppError
from services.base_service import BaseService


class AuthService(BaseService):
    def __init__(self, bcrypt_instance=None):
        super().__init__()
        self.repo = AuthRepository()
        self.login_repo = LoginHistoryRepository()
        self.bcrypt = bcrypt_instance or Bcrypt()

    def signup(self, data):
        self._validate_signup_data(data)
        self._check_user_exists(data["email"])
        password_hash = self._hash_password(data["password"])
        self.repo.create_user(data["username"], data["email"], password_hash)
        return self._create_success_response(message=messages.USER_REGISTERED)

    def login(self, data):
        self._validate_login_data(data)
        user = self._get_and_validate_user(data["email"], data["password"])
        token = self._generate_token(user)
        self.record_login(user["Id"])
        return self._create_success_response({
            "access_token": token,
            "username": user["Username"],
            "role": user["Role"]
        })

    def record_login(self, user_id):
        self.login_repo.record_login(user_id)

    def _validate_signup_data(self, data):
        self._validate_required_fields(
            data.get("username"), 
            data.get("email"), 
            data.get("password"),
            error_message="Missing required fields"
        )
        self._validate_email_format(data.get("email"))

    def _validate_login_data(self, data):
        self._validate_required_fields(
            data.get("email"), 
            data.get("password"),
            error_message="Missing required fields"
        )
        self._validate_email_format(data.get("email"))

    def _validate_email_format(self, email):
        if not email:
            return
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            raise AppError(messages.INVALID_EMAIL_FORMAT, HTTPStatus.BAD_REQUEST)

    def _check_user_exists(self, email):
        user_row = self.repo.get_user_by_email(email)
        if user_row:
            raise AppError(messages.USER_ALREADY_EXISTS, HTTPStatus.CONFLICT)

    def _hash_password(self, password):
        return self.bcrypt.generate_password_hash(password).decode("utf-8")

    def _get_and_validate_user(self, email, password):
        user_row = self.repo.get_user_by_email(email)
        user = self._format_user_data(user_row)
        
        if not user or not self.bcrypt.check_password_hash(user["PasswordHash"], password):
            raise AppError("Invalid credentials", HTTPStatus.UNAUTHORIZED)
        
        return user

    def _format_user_data(self, user_row):
        if not user_row:
            return None
        return {
            "Id": user_row.Id,
            "Username": user_row.Username,
            "Email": user_row.Email,
            "PasswordHash": user_row.PasswordHash,
            "Role": user_row.Role
        }

    def _generate_token(self, user):
        return create_access_token(
            identity=str(user["Id"]),
            additional_claims={"role": user["Role"]},
            expires_delta=timedelta(days=1)
        )
