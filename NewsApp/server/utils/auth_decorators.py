from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from http import HTTPStatus


class RoleRequired:
    def __init__(self, role):
        self.required_role = role

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            user_role = claims.get("role")
            if user_role != self.required_role:
                return jsonify({
                    "success": False,
                    "message": f"{self.required_role} access required"
                }), HTTPStatus.FORBIDDEN

            return fn(*args, **kwargs)
        return wrapper


admin_required = RoleRequired("Admin")
user_required = RoleRequired("User")
