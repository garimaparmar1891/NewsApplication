from flask import Blueprint
from flasgger import swag_from
from controllers.keyword_controller import KeywordController
from utils.auth_decorators import user_required

keyword_bp = Blueprint("keywords", __name__)
keyword_controller = KeywordController()

@keyword_bp.route("/api/keywords", methods=["GET"])
@user_required
@swag_from("../docs/keywords/get_keywords.yml")
def get_keywords():
    return keyword_controller.get_all_keywords()

@keyword_bp.route("/api/keywords", methods=["POST"])
@user_required
@swag_from("../docs/keywords/add_keyword.yml")
def add_keyword():
    return keyword_controller.add_keyword()

@keyword_bp.route("/api/keywords/<int:keyword_id>", methods=["DELETE"])
@user_required
@swag_from("../docs/keywords/delete_keyword.yml")
def delete_keyword(keyword_id):
    return keyword_controller.delete_keyword(keyword_id)
