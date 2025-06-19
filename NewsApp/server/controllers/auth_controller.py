from flask import request
from flask_jwt_extended import create_access_token
from datetime import timedelta
from services.auth_service import AuthService
from utils.response_utils import success_response, error_response
from http import HTTPStatus


class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    # ---------- Signup/Login ----------
    def signup(self):
        data = request.get_json()
        if not self._has_required_fields(data, ["username", "email", "password"]):
            return self._error("Missing required fields")

        return self._process_signup(data)

    def login(self):
        data = request.get_json()
        if not self._has_required_fields(data, ["email", "password"]):
            return self._error("Missing credentials")

        return self._process_login(data)


    # ---------- Private Helpers ----------
    def _process_signup(self, data):
        result = self.auth_service.signup(
            username=data["username"],
            email=data["email"],
            password=data["password"]
        )
        print(result)
        if result.get("error"):
            return error_response(result["error"], result.get("status", HTTPStatus.BAD_REQUEST))

        return success_response(message="Signup successful", status=HTTPStatus.CREATED)

    def _process_login(self, data):
        user = self.auth_service.login(data["email"], data["password"])
        if not user:
            return error_response("Invalid credentials", HTTPStatus.UNAUTHORIZED)

        token = self._generate_token(user)
        self.auth_service.record_login(user["Id"])

        return success_response({
            "access_token": token,
            "username": user["Username"],
            "role": user["Role"]
        })

    def _generate_token(self, user):
        return create_access_token(
            identity=str(user["Id"]),
            additional_claims={"role": user["Role"]},
            expires_delta=timedelta(days=1)
        )

    def _has_required_fields(self, data, required):
        return all(data.get(field) for field in required)

    def _error(self, message, status=HTTPStatus.BAD_REQUEST):
        return error_response(message, status)
