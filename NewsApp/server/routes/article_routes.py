from flask import Blueprint
from flasgger import swag_from
from controllers.article_controller import ArticleController
from utils.auth_decorators import user_required

article_bp = Blueprint("articles", __name__)
article_controller = ArticleController()

# ---------- Search Articles ----------
@article_bp.route("/api/articles/search", methods=["GET"])
@user_required
@swag_from("../docs/articles/search_articles.yml")
def search_articles():
    return article_controller.search_articles_by_keyword_and_range()

# ---------- Get Today's Headlines ----------
@article_bp.route("/api/articles/today", methods=["GET"])
@user_required
@swag_from("../docs/articles/get_today_headlines.yml")
def get_today_headlines():
    return article_controller.get_today_headlines()

# ---------- Get Articles by Date Range ----------
@article_bp.route("/api/articles/range", methods=["GET"])
@user_required
@swag_from("../docs/articles/get_articles_by_range.yml")
def get_articles_by_range():
    return article_controller.get_articles_by_range()

# ---------- Get All Categories ----------
@article_bp.route("/api/categories", methods=["GET"])
@user_required
@swag_from("../docs/articles/get_all_categories.yml")
def get_all_categories():
    return article_controller.get_all_categories()

# ---------- Record Read Article ----------
@article_bp.route("/api/history/<int:article_id>", methods=["POST"])
@user_required
def record_article_read(article_id):
    return article_controller.record_article_read(article_id)
