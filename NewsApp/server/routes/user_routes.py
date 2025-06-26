from flask import Blueprint
from flasgger import swag_from
from controllers.user_controller import UserController
from utils.auth_decorators import user_required

user_bp = Blueprint("user", __name__)
user_controller = UserController()

# -------- user acticle actions ----------
@user_bp.route("/api/articles/<int:article_id>/save", methods=["POST"])
@user_required
@swag_from("../docs/articles/save_article.yml")
def save_article(article_id):
    return user_controller.save_article(article_id)

@user_bp.route("/api/users/saved-articles", methods=["GET"])
@user_required
@swag_from("../docs/users/get_saved_articles.yml")
def get_saved_articles():
    return user_controller.get_saved_articles()

@user_bp.route("/api/articles/<int:article_id>/unsave", methods=["DELETE"])
@user_required
@swag_from("../docs/users/unsave_article.yml")
def unsave_article(article_id):
    return user_controller.unsave_article(article_id)
