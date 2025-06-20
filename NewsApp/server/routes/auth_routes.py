from flask import Blueprint
from controllers.auth_controller import AuthController
from flasgger import swag_from

auth_bp = Blueprint("auth", __name__)
auth_controller = AuthController()

# ---------- User Signup ----------
@auth_bp.route("/api/signup", methods=["POST"])
@swag_from("../docs/auth/signup.yml")
def signup():
    return auth_controller.signup()

# ---------- User Login ----------
@auth_bp.route("/api/login", methods=["POST"])
@swag_from("../docs/auth/login.yml")
def login():
    return auth_controller.login()
