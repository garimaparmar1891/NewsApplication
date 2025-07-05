from flask import Blueprint
from flasgger import swag_from
from controllers.keyword_controller import KeywordController
from utils.auth_decorators import admin_required

keyword_bp = Blueprint("keywords", __name__)
keyword_controller = KeywordController()

@keyword_bp.route("/api/keywords", methods=["GET"])
@admin_required
@swag_from("../docs/admin/get_keywords.yml")
def get_keywords():
    return keyword_controller.get_keywords()

@keyword_bp.route("/api/keywords", methods=["POST"])
@admin_required
@swag_from("../docs/admin/add_keyword.yml")
def add_keyword():
    return keyword_controller.add_keyword()

@keyword_bp.route("/api/keywords/<string:word>", methods=["DELETE"])
@admin_required
@swag_from("../docs/admin/delete_keyword.yml")
def delete_keyword(word):
    return keyword_controller.delete_keyword(word)
