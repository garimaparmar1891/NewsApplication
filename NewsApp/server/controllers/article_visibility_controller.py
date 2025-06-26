# currently working
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from services.article_visibility_service import ArticleModerationService

moderation_service = ArticleModerationService()

class ArticleModerationController:

    def report_article(self, article_id):
        user_id = get_jwt_identity()
        reason = request.json.get("reason")
        if not reason:
            return jsonify({"message": "Reason is required"}), 400
        success = moderation_service.report_article(user_id, article_id, reason)
        return (jsonify({"message": "Reported"}), 200) if success else (jsonify({"message": "Error"}), 500)

    def get_reported_articles(self):
        return jsonify({"data": moderation_service.get_reported_articles()})

    def hide_article(self, article_id):
        moderation_service.set_article_visibility(article_id, hide=True)
        return jsonify({"message": "Article hidden"})

    def unhide_article(self, article_id):
        moderation_service.set_article_visibility(article_id, hide=False)
        return jsonify({"message": "Article visible"})

    def hide_category(self, category_id):
        moderation_service.set_category_visibility(category_id, hide=True)
        return jsonify({"message": "Category hidden"})

    def unhide_category(self, category_id):
        moderation_service.set_category_visibility(category_id, hide=False)
        return jsonify({"message": "Category visible"})

    def add_blocked_keyword(self):
        keyword = request.json.get("keyword")
        if not keyword:
            return jsonify({"message": "Keyword required"}), 400
        moderation_service.add_blocked_keyword(keyword)
        return jsonify({"message": "Keyword blocked"})

    def get_blocked_keywords(self):
        return jsonify({"data": moderation_service.get_blocked_keywords()})
