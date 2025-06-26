from flask import Blueprint
from controllers.user_keyword_controller import UserKeywordController
from utils.auth_decorators import user_required
from flasgger import swag_from

user_keyword_bp = Blueprint("user_keywords", __name__)
controller = UserKeywordController()

#---------- user keyword action --------
@user_keyword_bp.route("/api/user-keywords", methods=["POST"])
@user_required
@swag_from("../docs/keywords/add_user_keyword.yml")
def add_user_keyword():
    return controller.add_user_keyword()

@user_keyword_bp.route("/api/user-keywords", methods=["GET"])
@user_required
@swag_from("../docs/keywords/get_user_keywords.yml")
def get_user_keywords():
    return controller.get_user_keywords()

@user_keyword_bp.route("/api/user-keywords/<int:keyword_id>", methods=["DELETE"])
@user_required
@swag_from("../docs/keywords/delete_user_keyword.yml")
def delete_user_keyword(keyword_id):
    return controller.delete_user_keyword(keyword_id)
