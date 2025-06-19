from flask_bcrypt import Bcrypt
from repositories.user_repository import UserRepository
from repositories.login_history_repository import LoginHistoryRepository
from typing import Optional, Dict, Union


class AuthService:
    def __init__(self, bcrypt_instance: Optional[Bcrypt] = None):
        self.repo = UserRepository()
        self.login_repo = LoginHistoryRepository()
        self.bcrypt = bcrypt_instance or Bcrypt()

    def signup(self, username, email, password):
        if self.repo.get_user_by_email(email):
            return {"error": "User already exists", "status": 400}

        password_hash = self.bcrypt.generate_password_hash(password).decode("utf-8")
        self.repo.create_user(username, email, password_hash)

        return {"message": "User registered successfully", "status": 201}

    def login(self, email, password):
        user = self.repo.get_user_by_email(email)
        if user and self.bcrypt.check_password_hash(user["PasswordHash"], password):
            return user
        return None

    def record_login(self, user_id):
        self.login_repo.record_login(user_id)
