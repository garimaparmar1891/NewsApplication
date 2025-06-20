from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from http import HTTPStatus


class RoleRequired:
    def __init__(self, role):
        self.role = role

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not self._has_required_role():
                return self._forbidden_response()
            return fn(*args, **kwargs)
        return wrapper

    def _has_required_role(self):
        verify_jwt_in_request()
        claims = get_jwt()
        return claims.get("role") == self.role

    def _forbidden_response(self):
        return jsonify({
            "success": False,
            "message": f"{self.role} access required"
        }), HTTPStatus.FORBIDDEN


admin_required = RoleRequired("Admin")
user_required = RoleRequired("User")
