from flask import Blueprint
from flasgger import swag_from
from controllers.article_visibility_controller import ArticleVisibilityController
from utils.auth_decorators import admin_required, user_required

article_visibility_bp = Blueprint("article_visibility", __name__)
article_visibility_controller = ArticleVisibilityController()

@article_visibility_bp.route("/api/article-visibility/report/<int:article_id>", methods=["POST"])
@user_required
@swag_from("../docs/article_visibility/report_article.yml")
def report_article(article_id):
    return article_visibility_controller.report_article(article_id)

@article_visibility_bp.route("/api/article-visibility/reports", methods=["GET"])
@admin_required
@swag_from("../docs/article_visibility/view_reports.yml")
def get_all_reported_articles():
    return article_visibility_controller.get_all_reported_articles()

@article_visibility_bp.route("/api/article-visibility/articles/<int:article_id>/<string:action>", methods=["PATCH"])
@admin_required
@swag_from("../docs/article_visibility/toggle_article_visibility.yml")
def toggle_article_visibility(article_id, action):
    return article_visibility_controller.toggle_article_visibility(article_id, action)

@article_visibility_bp.route("/api/article-visibility/categories/<int:category_id>/<string:action>", methods=["PATCH"])
@admin_required
@swag_from("../docs/article_visibility/toggle_category_visibility.yml")
def toggle_category_visibility(category_id, action):
    return article_visibility_controller.toggle_category_visibility(category_id, action)

@article_visibility_bp.route("/api/article-visibility/blocked-keywords", methods=["POST"])
@admin_required
@swag_from("../docs/article_visibility/add_blocked_keyword.yml")
def add_blocked_keyword():
    return article_visibility_controller.add_blocked_keyword()

@article_visibility_bp.route("/api/article-visibility/blocked-keywords", methods=["GET"])
@admin_required
@swag_from("../docs/article_visibility/get_blocked_keywords.yml")
def get_blocked_keywords():
    return article_visibility_controller.get_blocked_keywords()

@article_visibility_bp.route("/api/article-visibility/blocked-keywords/<int:keyword_id>", methods=["DELETE"])
@admin_required
@swag_from("../docs/article_visibility/delete_blocked_keyword.yml")
def delete_blocked_keyword(keyword_id):
    return article_visibility_controller.delete_blocked_keyword(keyword_id)
