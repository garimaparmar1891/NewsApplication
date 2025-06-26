from flask_bcrypt import Bcrypt
from repositories.auth_repository import AuthRepository
from repositories.login_history_repository import LoginHistoryRepository
from typing import Optional, Dict, Union
from http import HTTPStatus
from constants import messages


class AuthService:
    def __init__(self, bcrypt_instance: Optional[Bcrypt] = None):
        self.repo = AuthRepository()
        self.login_repo = LoginHistoryRepository()
        self.bcrypt = bcrypt_instance or Bcrypt()

    def signup(self, username, email, password):
        if self.repo.get_user_by_email(email):
            return {"error": messages.USER_ALREADY_EXISTS, "status": HTTPStatus.BAD_REQUEST}

        password_hash = self.bcrypt.generate_password_hash(password).decode("utf-8")
        self.repo.create_user(username, email, password_hash)

        return {"message": messages.USER_REGISTERED, "status": HTTPStatus.CREATED}

    def login(self, email, password):
        user = self.repo.get_user_by_email(email)
        if user and self.bcrypt.check_password_hash(user["PasswordHash"], password):
            return user
        return None

    def record_login(self, user_id):
        self.login_repo.record_login(user_id)
