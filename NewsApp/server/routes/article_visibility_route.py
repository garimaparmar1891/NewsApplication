from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.article_visibility_controller import ArticleModerationController
from utils.auth_decorators import admin_required

article_visibility_bp = Blueprint("moderation", __name__)
controller = ArticleModerationController()

# ---------- User report ---------
@article_visibility_bp.route("/api/articles/<int:article_id>/report", methods=["POST"])
@jwt_required()
def report_article(article_id):
    return controller.report_article(article_id)

# -------- Admin-only endpoints ----------
@article_visibility_bp.route("/api/admin/reports", methods=["GET"])
@admin_required
def get_reported_articles():
    return controller.get_reported_articles()

@article_visibility_bp.route("/api/admin/articles/<int:article_id>/hide", methods=["PATCH"])
@admin_required
def hide_article(article_id):
    return controller.hide_article(article_id)

@article_visibility_bp.route("/api/admin/articles/<int:article_id>/unhide", methods=["PATCH"])
@admin_required
def unhide_article(article_id):
    return controller.unhide_article(article_id)

@article_visibility_bp.route("/api/admin/categories/<int:category_id>/hide", methods=["PATCH"])
@admin_required
def hide_category(category_id):
    return controller.hide_category(category_id)

@article_visibility_bp.route("/api/admin/categories/<int:category_id>/unhide", methods=["PATCH"])
@admin_required
def unhide_category(category_id):
    return controller.unhide_category(category_id)

@article_visibility_bp.route("/api/admin/blocked-keywords", methods=["POST"])
@admin_required
def add_blocked_keyword():
    return controller.add_blocked_keyword()

@article_visibility_bp.route("/api/admin/blocked-keywords", methods=["GET"])
@admin_required
def list_blocked_keywords():
    return controller.get_blocked_keywords()
